(function () {
  "use strict";

  const state = {
    mission1: { cpuDone: false, gpuDone: false, completed: false },
    mission2: { answers: {}, completed: false },
    mission3: {
      batchSize: 8,
      preloadMode: "once",
      sawOom: false,
      sawOptimal: false,
      completed: false,
      running: false,
    },
  };

  const TENSOR_BLOCKS = 64;

  // Mission 2 Pipeline Tasks
  const PIPELINE_TASKS = [
    {
      id: "s3_list",
      title: "1. List & Download Vendor Photos from Amazon S3 (`photos.py`)",
      desc: "Open HTTPS connections, paginate S3 object keys under `images/<stem>/`, and stream bytes into memory.",
      correct: "CPU",
      whyOk: "Correct — Network I/O, TLS handshakes, and S3 API calls are sequential OS tasks handled by the Host CPU.",
      whyBad: "Not GPU work — A GPU has no network stack or filesystem driver; making a GPU wait on S3 downloads wastes expensive accelerator time.",
    },
    {
      id: "jpeg_decode",
      title: "2. Decode JPEG/PNG Files & Check File Extensions",
      desc: "Filter `.jpg`/`.png` extensions, parse file headers, and unpack compressed bytes into RGB arrays.",
      correct: "CPU",
      whyOk: "Correct — Branching rules (`.jpg` vs `.gif`) and file parsing live in Host CPU and System RAM before tensors move to the device.",
      whyBad: "Not GPU work — File extension checks and standard image loading happen on the Host CPU before copying tensors over PCIe.",
    },
    {
      id: "blip_vision",
      title: "3. Run Vision Transformer Layers Across Image Patch Grids (`describe_items.py`)",
      desc: "Multiply and add millions of weight and activation values across every pixel patch in the micro-batch.",
      correct: "GPU",
      whyOk: "Correct — Dense, uniform matrix multiplication across thousands of tensor elements is exactly what GPU Streaming Multiprocessors and Tensor Cores are built for.",
      whyBad: "Too slow on CPU — Running deep vision layers sequentially on 4 CPU cores creates the exact bottleneck we are trying to avoid.",
    },
    {
      id: "blip_tokens",
      title: "4. Compute Next-Word Probabilities for Caption Generation",
      desc: "Run parallel matrix math in the BLIP language decoder to emit tokens like 'a plate of ramen noodles'.",
      correct: "GPU",
      whyOk: "Correct — Decoder forward passes are heavy tensor operations that run in VRAM alongside the loaded model weights.",
      whyBad: "Too slow on CPU — Token probability projections multiply large weight matrices that belong on the GPU.",
    },
    {
      id: "accept_rule",
      title: "5. Apply KodeFood Business Rule (`accepted` vs `rejected`)",
      desc: "Check if the short caption contains food keywords or non-food words (selfie, car, logo).",
      correct: "CPU",
      whyOk: "Correct — Checking string keywords and branching on an `if/else` rule takes microseconds on the Host CPU.",
      whyBad: "Not GPU work — Simple string matching and branching logic do not benefit from thousands of parallel math cores.",
    },
    {
      id: "csv_upload",
      title: "6. Assemble `descriptions.csv` and Upload to S3 Output Bucket",
      desc: "Format CSV rows (`image_s3_uri,item_description,photo_status`) and call `PutObject` to S3.",
      correct: "CPU",
      whyOk: "Correct — Formatting text rows and uploading the final artifact back to S3 is Host CPU orchestration.",
      whyBad: "Not GPU work — Once tensor inference finishes, captions return to Host RAM so the CPU can write and upload the CSV.",
    },
  ];

  // DOM Elements
  const stepTabs = document.querySelectorAll(".step-tab");
  const panels = {
    1: document.getElementById("mission-1"),
    2: document.getElementById("mission-2"),
    3: document.getElementById("mission-3"),
  };

  function switchStep(stepNum) {
    stepTabs.forEach((t) => {
      t.classList.toggle("active", Number(t.dataset.step) === stepNum);
    });
    Object.keys(panels).forEach((k) => {
      panels[k].classList.toggle("hidden", Number(k) !== stepNum);
    });
  }

  stepTabs.forEach((tab) => {
    tab.addEventListener("click", () => switchStep(Number(tab.dataset.step)));
  });

  document.getElementById("next-to-m2").addEventListener("click", () => switchStep(2));
  document.getElementById("next-to-m3").addEventListener("click", () => switchStep(3));

  function updateGlobalProgress() {
    const doneCount =
      (state.mission1.completed ? 1 : 0) +
      (state.mission2.completed ? 1 : 0) +
      (state.mission3.completed ? 1 : 0);

    const pill = document.getElementById("overall-progress-pill");
    pill.textContent = `${doneCount} / 3 Missions Complete`;
    pill.classList.toggle("all-done", doneCount === 3);

    const setBadge = (num, isDone) => {
      const el = document.getElementById(`status-${num}`);
      el.textContent = isDone ? "Complete" : "Pending";
      el.classList.toggle("done", isDone);
    };
    setBadge(1, state.mission1.completed);
    setBadge(2, state.mission2.completed);
    setBadge(3, state.mission3.completed);

    document
      .getElementById("completion-banner")
      .classList.toggle("hidden", doneCount !== 3);
  }

  // ==================== MISSION 1 LOGIC ====================
  const cpuGrid = document.getElementById("cpu-grid");
  const gpuGrid = document.getElementById("gpu-grid");

  function buildTensorGrid(container, prefix) {
    container.innerHTML = "";
    for (let i = 0; i < TENSOR_BLOCKS; i++) {
      const cell = document.createElement("div");
      cell.className = "tensor-cell";
      cell.id = `${prefix}-cell-${i}`;
      // deterministic pseudo pixel value
      const val = ((i * 37 + 19) % 90) + 10;
      cell.textContent = `0.${val}`;
      container.appendChild(cell);
    }
  }

  buildTensorGrid(cpuGrid, "cpu");
  buildTensorGrid(gpuGrid, "gpu");

  let cpuTimer = null;
  let gpuTimer = null;

  document.getElementById("run-cpu-btn").addEventListener("click", () => {
    if (cpuTimer) clearInterval(cpuTimer);
    buildTensorGrid(cpuGrid, "cpu");
    const btn = document.getElementById("run-cpu-btn");
    btn.disabled = true;

    let idx = 0;
    let elapsed = 0;
    const cores = 4;

    cpuTimer = setInterval(() => {
      for (let i = 0; i < TENSOR_BLOCKS; i++) {
        const c = document.getElementById(`cpu-cell-${i}`);
        c.classList.remove("active-cpu");
      }

      if (idx >= TENSOR_BLOCKS) {
        clearInterval(cpuTimer);
        cpuTimer = null;
        btn.disabled = false;
        state.mission1.cpuDone = true;
        document.getElementById("cpu-note").innerHTML =
          "<strong>CPU Finished (1,280 ms):</strong> 4 cores had to step through 16 sequential waves (4 blocks at a time).";
        checkMission1Complete();
        return;
      }

      for (let c = 0; c < cores && idx < TENSOR_BLOCKS; c++, idx++) {
        const cell = document.getElementById(`cpu-cell-${idx}`);
        cell.classList.add("active-cpu", "done-cpu");
      }

      elapsed += 80;
      document.getElementById("cpu-blocks-done").textContent = `${idx} / ${TENSOR_BLOCKS}`;
      document.getElementById("cpu-time-ms").textContent = `${elapsed} ms`;
    }, 140);
  });

  document.getElementById("run-gpu-btn").addEventListener("click", () => {
    if (gpuTimer) clearInterval(gpuTimer);
    buildTensorGrid(gpuGrid, "gpu");
    const btn = document.getElementById("run-gpu-btn");
    btn.disabled = true;

    let wave = 0;
    const blocksPerWave = 32; // 2 waves of 32 parallel blocks
    let elapsed = 0;

    gpuTimer = setInterval(() => {
      for (let i = 0; i < TENSOR_BLOCKS; i++) {
        document.getElementById(`gpu-cell-${i}`).classList.remove("active-gpu");
      }

      if (wave * blocksPerWave >= TENSOR_BLOCKS) {
        clearInterval(gpuTimer);
        gpuTimer = null;
        btn.disabled = false;
        state.mission1.gpuDone = true;
        document.getElementById("gpu-note").innerHTML =
          "<strong>GPU Finished (90 ms):</strong> Parallel cores swept through all 64 tensor blocks in two wide waves (~14x faster).";
        checkMission1Complete();
        return;
      }

      const start = wave * blocksPerWave;
      const end = Math.min(TENSOR_BLOCKS, start + blocksPerWave);
      for (let i = start; i < end; i++) {
        const cell = document.getElementById(`gpu-cell-${i}`);
        cell.classList.add("active-gpu", "done-gpu");
      }

      wave++;
      elapsed += 45;
      document.getElementById("gpu-blocks-done").textContent = `${end} / ${TENSOR_BLOCKS}`;
      document.getElementById("gpu-time-ms").textContent = `${elapsed} ms`;
    }, 220);
  });

  function checkMission1Complete() {
    if (state.mission1.cpuDone && state.mission1.gpuDone) {
      state.mission1.completed = true;
      document.getElementById("m1-insight").innerHTML =
        "<strong>Mission 1 Complete!</strong> Takeaway: When the job is the exact same matrix math across thousands of pixel values, parallel GPU cores finish the folder in a fraction of the time.";
      updateGlobalProgress();
    }
  }

  // ==================== MISSION 2 LOGIC ====================
  const tasksContainer = document.getElementById("tasks-container");

  function renderMission2() {
    tasksContainer.innerHTML = "";
    let correctCount = 0;

    PIPELINE_TASKS.forEach((task) => {
      const picked = state.mission2.answers[task.id];
      const isCorrect = picked === task.correct;
      if (isCorrect) correctCount++;

      const row = document.createElement("div");
      row.className = "task-row";
      if (picked) {
        row.classList.add(isCorrect ? "correct" : "wrong");
      }

      let feedbackHtml = "";
      if (picked) {
        feedbackHtml = `<div class="task-feedback ${isCorrect ? "ok" : "bad"}">${
          isCorrect ? task.whyOk : task.whyBad
        }</div>`;
      }

      row.innerHTML = `
        <div class="task-main">
          <p class="task-title">${task.title}</p>
          <p class="task-desc">${task.desc}</p>
          ${feedbackHtml}
        </div>
        <div class="task-actions">
          <button type="button" class="choice-btn ${
            picked === "CPU" ? (isCorrect ? "selected-ok" : "selected-bad") : ""
          }" data-task="${task.id}" data-choice="CPU">Host CPU + RAM</button>
          <button type="button" class="choice-btn ${
            picked === "GPU" ? (isCorrect ? "selected-ok" : "selected-bad") : ""
          }" data-task="${task.id}" data-choice="GPU">NVIDIA GPU + VRAM</button>
        </div>
      `;
      tasksContainer.appendChild(row);
    });

    document.getElementById("routed-count").textContent = `${correctCount} / ${PIPELINE_TASKS.length}`;

    if (correctCount === PIPELINE_TASKS.length) {
      state.mission2.completed = true;
      document.getElementById("m2-insight").innerHTML =
        "<strong>Mission 2 Complete!</strong> Takeaway: The CPU moves data, decodes files, and enforces business rules (`photos.py`); the GPU crunches tensors (`describe_items.py`). If S3 downloads are slow, the GPU sits idle while you pay GPU prices.";
      updateGlobalProgress();
    }

    tasksContainer.querySelectorAll(".choice-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.mission2.answers[btn.dataset.task] = btn.dataset.choice;
        renderMission2();
      });
    });
  }

  document.getElementById("reset-m2-btn").addEventListener("click", () => {
    state.mission2.answers = {};
    state.mission2.completed = false;
    renderMission2();
    updateGlobalProgress();
  });

  renderMission2();

  // ==================== MISSION 3 LOGIC ====================
  const batchButtons = document.querySelectorAll("#batch-size-buttons .pill-btn");
  const loadButtons = document.querySelectorAll("#model-load-buttons .pill-btn");

  batchButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (state.mission3.running) return;
      batchButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.mission3.batchSize = Number(btn.dataset.batch);
    });
  });

  loadButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (state.mission3.running) return;
      loadButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.mission3.preloadMode = btn.dataset.preload;
    });
  });

  // VRAM math model on a 16.0 GB NVIDIA T4:
  // Base BLIP weights + CUDA context = 3.6 GB VRAM
  // Each photo in active forward pass = 0.70 GB of intermediate activations
  // Batch 1  -> 3.6 + 0.7 = 4.3 GB (safe, 38% GPU util)
  // Batch 4  -> 3.6 + 2.8 = 6.4 GB (safe, 72% GPU util)
  // Batch 8  -> 3.6 + 5.6 = 9.2 GB (sweet spot, 92% GPU util)
  // Batch 16 -> 3.6 + 11.2 = 14.8 GB (tight warning, 95% GPU util)
  // Batch 30 -> 3.6 + 21.0 = 24.6 GB -> CUDA OOM CRASH (> 16.0 GB VRAM!)
  function calcVramGb(batchSize) {
    return +(3.6 + batchSize * 0.7).toFixed(1);
  }

  function calcGpuUtil(batchSize, preloadMode) {
    const base = { 1: 36, 4: 72, 8: 92, 16: 94, 30: 0 }[batchSize] || 50;
    return preloadMode === "every" ? Math.max(18, base - 45) : base;
  }

  let simInterval = null;

  document.getElementById("run-batch-sim-btn").addEventListener("click", () => {
    if (state.mission3.running) return;
    if (simInterval) clearInterval(simInterval);

    const batchSize = state.mission3.batchSize;
    const preloadMode = state.mission3.preloadMode;
    const totalPhotos = 30;
    const totalPasses = Math.ceil(totalPhotos / batchSize);
    const vramNeeded = calcVramGb(batchSize);
    const isOom = vramNeeded > 16.0;

    const gpuBox = document.getElementById("gpu-hw-box");
    const vramBar = document.getElementById("vram-bar");
    const vramText = document.getElementById("vram-text");
    const hostRamBar = document.getElementById("host-ram-bar");
    const hostRamText = document.getElementById("host-ram-text");
    const pcieEl = document.getElementById("pcie-indicator");
    const pcieText = document.getElementById("pcie-status-text");
    const logBox = document.getElementById("sim-log-box");
    const runBtn = document.getElementById("run-batch-sim-btn");

    state.mission3.running = true;
    runBtn.disabled = true;
    gpuBox.classList.remove("oom-crash");
    logBox.className = "sim-log";

    // Host RAM only changes slightly (4.2 GB base + ~0.05 GB per photo buffer)
    const hostRamUsed = +(4.2 + Math.min(batchSize, 30) * 0.04).toFixed(1);
    hostRamText.textContent = `${hostRamUsed} / 16.0 GB`;
    hostRamBar.style.width = `${(hostRamUsed / 16.0) * 100}%`;

    pcieEl.classList.add("active");
    pcieText.textContent =
      preloadMode === "once"
        ? "Copying BLIP weights once + streaming micro-batch tensors over PCIe..."
        : "WARNING: Re-copying 3.6 GB model weights over PCIe on every micro-batch!";

    if (isOom) {
      // Immediate OOM crash on Pass 1
      vramText.textContent = `${vramNeeded} / 16.0 GB (OVERFLOW!)`;
      vramBar.style.width = "100%";
      vramBar.className = "meter-fill bad";
      gpuBox.classList.add("oom-crash");
      document.getElementById("pass-counter").textContent = `1 / 1 (CRASHED)`;
      document.getElementById("photos-counter").textContent = `0 / 30`;
      document.getElementById("gpu-util-text").textContent = `0% (Aborted)`;

      logBox.className = "sim-log oom";
      logBox.innerHTML =
        `<strong>RuntimeError: CUDA out of memory!</strong> Tried to allocate ${vramNeeded} GB on a 16.0 GB NVIDIA T4 (` +
        `3.6 GB model weights + 21.0 GB activations for 30 photos at once). Notice that <strong>Host System RAM is only at ${hostRamUsed} / 16.0 GB</strong>—adding host RAM will never fix a GPU VRAM crash!`;

      state.mission3.sawOom = true;
      state.mission3.running = false;
      runBtn.disabled = false;
      pcieEl.classList.remove("active");
      updateMission3Checklist();
      return;
    }

    // Valid run across micro-batches
    const pct = Math.min(100, (vramNeeded / 16.0) * 100);
    vramText.textContent = `${vramNeeded} / 16.0 GB`;
    vramBar.style.width = `${pct}%`;
    vramBar.className = `meter-fill ${vramNeeded > 14 ? "warn" : "ok"}`;

    let currentPass = 0;
    const util = calcGpuUtil(batchSize, preloadMode);
    document.getElementById("gpu-util-text").textContent = `${util}%`;

    logBox.innerHTML = `Running ${totalPhotos} vendor photos in <strong>${totalPasses} micro-batch passes</strong> (batch size ${batchSize})...`;

    simInterval = setInterval(() => {
      currentPass++;
      const processed = Math.min(totalPhotos, currentPass * batchSize);
      document.getElementById("pass-counter").textContent = `${currentPass} / ${totalPasses}`;
      document.getElementById("photos-counter").textContent = `${processed} / ${totalPhotos}`;

      if (currentPass >= totalPasses) {
        clearInterval(simInterval);
        simInterval = null;
        state.mission3.running = false;
        runBtn.disabled = false;
        pcieEl.classList.remove("active");
        pcieText.textContent = "Transfer complete — descriptions.csv written to S3";

        logBox.className = "sim-log success";
        if (batchSize === 8 && preloadMode === "once") {
          state.mission3.sawOptimal = true;
          logBox.innerHTML =
            `<strong>SUCCEEDED (Optimal Production Profile):</strong> 30 photos processed in 4 micro-batches (8 + 8 + 8 + 6). ` +
            `VRAM stayed safely at <strong>9.2 / 16.0 GB</strong>, model weights loaded once over PCIe, and GPU utilization hit <strong>92%</strong>.`;
        } else if (preloadMode === "every") {
          logBox.innerHTML =
            `<strong>SUCCEEDED (PCIe Bottleneck):</strong> Job finished, but reloading model weights across the PCIe bus on every batch dropped GPU utilization to <strong>${util}%</strong>.`;
        } else if (batchSize === 1) {
          logBox.innerHTML =
            `<strong>SUCCEEDED (Under-utilized GPU):</strong> Processing 1 photo at a time used only 4.3 GB VRAM, but took 30 separate passes and left the T4 at <strong>${util}% utilization</strong>.`;
        } else {
          logBox.innerHTML =
            `<strong>SUCCEEDED:</strong> Completed 30 photos in ${totalPasses} passes using ${vramNeeded} / 16.0 GB VRAM (${util}% GPU utilization).`;
        }
        updateMission3Checklist();
      }
    }, 220);
  });

  function updateMission3Checklist() {
    const oomEl = document.getElementById("chk-oom");
    const optEl = document.getElementById("chk-opt");

    if (state.mission3.sawOom) {
      oomEl.classList.add("done");
      oomEl.innerHTML = "✓ Triggered and observed a <strong>VRAM Out-of-Memory (`BATCH_SIZE=30`)</strong> crash";
    }
    if (state.mission3.sawOptimal) {
      optEl.classList.add("done");
      optEl.innerHTML = "✓ Completed a healthy high-utilization run with <strong>`BATCH_SIZE=8` (Load weights once)</strong>";
    }

    if (state.mission3.sawOom && state.mission3.sawOptimal) {
      state.mission3.completed = true;
      document.getElementById("m3-insight").innerHTML =
        "<strong>Mission 3 Complete!</strong> Takeaway: VRAM is physically separate from Host RAM. Micro-batching (`BATCH_SIZE=8`) keeps the NVIDIA T4 productive without crossing its 16 GB VRAM ceiling.";
      updateGlobalProgress();
    }
  }

  // Reset All
  document.getElementById("reset-all-btn").addEventListener("click", () => {
    window.location.reload();
  });
})();
