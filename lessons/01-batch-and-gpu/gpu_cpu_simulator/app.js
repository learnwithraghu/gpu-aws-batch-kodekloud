(function () {
  "use strict";

  const state = {
    gridN: 8,
    viewMode: "visual",
    selected: null,
    pixels: [], // {r,g,b} length gridN*gridN
    activations: [],
    layerStep: 0,
    checkpoints: { inspect: false, cpu: false, gpu: false },
    execBlocks: 64,
    cpu: { idx: 0, tick: 0, elapsed: 0, playing: false, done: false },
    gpu: { wave: 0, elapsed: 0, playing: false, done: false, pcieDone: false },
  };

  // Deterministic “dish” palette: plate + food + sauce patches
  function buildDishPixels(n) {
    const pixels = [];
    const cx = (n - 1) / 2;
    const cy = (n - 1) / 2;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const dx = (c - cx) / n;
        const dy = (r - cy) / n;
        const dist = Math.sqrt(dx * dx + dy * dy);
        let red, green, blue;
        if (dist > 0.48) {
          // dark table
          red = 28 + ((r * 3 + c) % 12);
          green = 32 + ((r + c * 2) % 10);
          blue = 40 + ((r * 2 + c) % 14);
        } else if (dist > 0.38) {
          // plate rim
          red = 210 + ((r + c) % 20);
          green = 205 + ((r * 2) % 18);
          blue = 190 + ((c * 3) % 16);
        } else if ((r + c * 3) % 7 === 0) {
          // greens / herbs
          red = 50 + (r % 30);
          green = 140 + (c % 40);
          blue = 60 + ((r + c) % 25);
        } else if ((r * 5 + c) % 11 < 3) {
          // sauce / red
          red = 180 + (c % 40);
          green = 55 + (r % 30);
          blue = 45 + ((r + c) % 20);
        } else {
          // noodles / warm food
          red = 200 + ((r * 7 + c) % 35);
          green = 150 + ((c * 5 + r) % 40);
          blue = 70 + ((r + c * 3) % 30);
        }
        pixels.push({
          r: Math.min(255, red),
          g: Math.min(255, green),
          b: Math.min(255, blue),
        });
      }
    }
    return pixels;
  }

  // Shared layer weights (same formula on every patch)
  const WEIGHTS = { wr: 0.35, wg: 0.45, wb: 0.2, bias: -0.12 };

  function activationFor(pixel) {
    const rn = pixel.r / 255;
    const gn = pixel.g / 255;
    const bn = pixel.b / 255;
    const out = rn * WEIGHTS.wr + gn * WEIGHTS.wg + bn * WEIGHTS.wb + WEIGHTS.bias;
    return Math.max(0, Math.min(1, out));
  }

  function speedMs() {
    const v = document.getElementById("speed-select").value;
    if (v === "slow") return 220;
    if (v === "fast") return 55;
    return 110;
  }

  function updateProgress() {
    const done =
      (state.checkpoints.inspect ? 1 : 0) +
      (state.checkpoints.cpu ? 1 : 0) +
      (state.checkpoints.gpu ? 1 : 0);
    const pill = document.getElementById("overall-progress-pill");
    pill.textContent = `${done} / 3 Checkpoints`;
    pill.classList.toggle("all-done", done === 3);
    document.getElementById("chk-inspect").classList.toggle("done", state.checkpoints.inspect);
    document.getElementById("chk-cpu").classList.toggle("done", state.checkpoints.cpu);
    document.getElementById("chk-gpu").classList.toggle("done", state.checkpoints.gpu);
    document.getElementById("completion-banner").classList.toggle("hidden", done !== 3);
  }

  // ---- Stage 1: dish canvas + inspect ----
  const canvas = document.getElementById("dish-canvas");
  const ctx = canvas.getContext("2d");
  const gridEl = document.getElementById("pixel-grid");

  function drawDish() {
    const n = state.gridN;
    const size = canvas.width;
    const cell = size / n;
    ctx.clearRect(0, 0, size, size);
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const p = state.pixels[r * n + c];
        ctx.fillStyle = `rgb(${p.r},${p.g},${p.b})`;
        ctx.fillRect(c * cell, r * cell, cell + 0.5, cell + 0.5);
      }
    }
  }

  function rebuildGridOverlay() {
    const n = state.gridN;
    gridEl.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
    gridEl.style.gridTemplateRows = `repeat(${n}, 1fr)`;
    gridEl.className = `grid-overlay mode-${state.viewMode === "visual" ? "visual" : state.viewMode}`;
    gridEl.innerHTML = "";
    for (let i = 0; i < n * n; i++) {
      const cell = document.createElement("div");
      cell.className = "grid-cell";
      cell.dataset.idx = String(i);
      const p = state.pixels[i];
      if (state.viewMode === "rgb") {
        cell.textContent = `${p.r}`;
        cell.title = `RGB(${p.r}, ${p.g}, ${p.b})`;
      } else if (state.viewMode === "tensor") {
        cell.textContent = (p.r / 255).toFixed(2);
        cell.title = `[${(p.r / 255).toFixed(2)}, ${(p.g / 255).toFixed(2)}, ${(p.b / 255).toFixed(2)}]`;
      }
      if (state.selected === i) cell.classList.add("selected");
      cell.addEventListener("click", () => selectPatch(i));
      gridEl.appendChild(cell);
    }
  }

  function selectPatch(idx) {
    state.selected = idx;
    state.checkpoints.inspect = true;
    updateProgress();
    rebuildGridOverlay();

    const n = state.gridN;
    const r = Math.floor(idx / n);
    const c = idx % n;
    const p = state.pixels[idx];
    document.getElementById("inspector-empty").classList.add("hidden");
    document.getElementById("inspector-body").classList.remove("hidden");
    document.getElementById("inspect-swatch").style.background = `rgb(${p.r},${p.g},${p.b})`;
    document.getElementById("inspect-coord").textContent = `Patch (${r}, ${c}) · index ${idx}`;
    document.getElementById("inspect-shape").textContent = `Shape: [3, ${n}, ${n}]  (channels × height × width)`;
    document.getElementById("val-r-raw").textContent = String(p.r);
    document.getElementById("val-g-raw").textContent = String(p.g);
    document.getElementById("val-b-raw").textContent = String(p.b);
    document.getElementById("val-r-f").textContent = (p.r / 255).toFixed(3);
    document.getElementById("val-g-f").textContent = (p.g / 255).toFixed(3);
    document.getElementById("val-b-f").textContent = (p.b / 255).toFixed(3);
  }

  function resetPixels(n) {
    state.gridN = n;
    state.pixels = buildDishPixels(n);
    state.selected = null;
    state.activations = new Array(n * n).fill(null);
    state.layerStep = 0;
    document.getElementById("inspector-empty").classList.remove("hidden");
    document.getElementById("inspector-body").classList.add("hidden");
    drawDish();
    rebuildGridOverlay();
    renderActivationGrid();
    resetCpu();
    resetGpu();
    syncExecBlocksToGrid();
  }

  document.querySelectorAll("#grid-size-buttons .pill-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#grid-size-buttons .pill-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      resetPixels(Number(btn.dataset.grid));
    });
  });

  document.querySelectorAll("#view-mode-buttons .pill-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#view-mode-buttons .pill-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.viewMode = btn.dataset.view;
      rebuildGridOverlay();
    });
  });

  // ---- Stage 2: layer math ----
  function renderActivationGrid() {
    const n = state.gridN;
    const grid = document.getElementById("activation-grid");
    grid.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
    grid.innerHTML = "";
    for (let i = 0; i < n * n; i++) {
      const cell = document.createElement("div");
      cell.className = "act-cell";
      const a = state.activations[i];
      if (a !== null && a !== undefined) {
        const v = Math.round(40 + a * 180);
        cell.style.background = `rgb(${v}, ${Math.round(v * 0.55)}, 40)`;
        cell.classList.add("done");
      }
      if (state.layerStep - 1 === i) cell.classList.add("active");
      grid.appendChild(cell);
    }
  }

  function stepOneBlock() {
    const n = state.gridN;
    const total = n * n;
    let idx = state.selected;
    if (idx === null || state.activations[idx] !== null) {
      idx = state.activations.findIndex((a) => a === null);
      if (idx < 0) idx = 0;
    }
    const p = state.pixels[idx];
    const out = activationFor(p);
    state.activations[idx] = out;
    state.layerStep = idx + 1;
    state.selected = idx;
    selectPatch(idx);

    const rn = (p.r / 255).toFixed(3);
    const gn = (p.g / 255).toFixed(3);
    const bn = (p.b / 255).toFixed(3);
    document.getElementById("layer-log").innerHTML =
      `<strong>Block ${idx}:</strong> (${rn}·${WEIGHTS.wr} + ${gn}·${WEIGHTS.wg} + ${bn}·${WEIGHTS.wb}) + (${WEIGHTS.bias}) = <strong>${out.toFixed(3)}</strong>. ` +
      `Same formula on every patch — no branching.`;
    renderActivationGrid();
  }

  function applyLayerAll() {
    const n = state.gridN;
    for (let i = 0; i < n * n; i++) {
      state.activations[i] = activationFor(state.pixels[i]);
    }
    state.layerStep = n * n;
    document.getElementById("layer-log").innerHTML =
      `<strong>Full layer applied</strong> to ${n * n} patches with one shared weight set. ` +
      `This is the same uniform math GPUs were built to run across millions of pixels (and later, tensors).`;
    renderActivationGrid();
  }

  document.getElementById("step-one-block-btn").addEventListener("click", stepOneBlock);
  document.getElementById("apply-layer-btn").addEventListener("click", applyLayerAll);
  document.getElementById("reset-layer-btn").addEventListener("click", () => {
    state.activations = new Array(state.gridN * state.gridN).fill(null);
    state.layerStep = 0;
    document.getElementById("layer-log").textContent =
      "Select a patch in Stage 1 (or click Step 1 Block) to watch one multiply-and-add on its [R, G, B] values.";
    renderActivationGrid();
  });

  // ---- Stage 3: CPU vs GPU ----
  const cpuGrid = document.getElementById("cpu-grid");
  const gpuGrid = document.getElementById("gpu-grid");
  let cpuTimer = null;
  let gpuTimer = null;

  function syncExecBlocksToGrid() {
    // Keep exec size independent but default to grid cells when matching
    const n = state.gridN;
    if (n === 8) state.execBlocks = 64;
    if (n === 16) state.execBlocks = 256;
    document.querySelectorAll("#exec-size-buttons .pill-btn").forEach((b) => {
      b.classList.toggle("active", Number(b.dataset.blocks) === state.execBlocks);
    });
    rebuildExecGrids();
  }

  function rebuildExecGrids() {
    const count = state.execBlocks;
    const cols = Math.sqrt(count);
    cpuGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    gpuGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    cpuGrid.innerHTML = "";
    gpuGrid.innerHTML = "";
    for (let i = 0; i < count; i++) {
      const c = document.createElement("div");
      c.className = "tensor-cell";
      c.id = `cpu-cell-${i}`;
      cpuGrid.appendChild(c);
      const g = document.createElement("div");
      g.className = "tensor-cell";
      g.id = `gpu-cell-${i}`;
      gpuGrid.appendChild(g);
    }
    document.getElementById("cpu-blocks-done").textContent = `0 / ${count}`;
    document.getElementById("gpu-blocks-done").textContent = `0 / ${count}`;
  }

  function resetCpu() {
    if (cpuTimer) {
      clearInterval(cpuTimer);
      cpuTimer = null;
    }
    state.cpu = { idx: 0, tick: 0, elapsed: 0, playing: false, done: false };
    document.getElementById("cpu-tick").textContent = "0";
    document.getElementById("cpu-time-ms").textContent = "0 ms";
    document.getElementById("cpu-blocks-done").textContent = `0 / ${state.execBlocks}`;
    document.getElementById("cpu-note").textContent =
      "Use Step to march 4 cores across the grid, or Play to run the full sequential pass.";
    document.querySelectorAll("#cpu-core-pills .core-pill").forEach((p) => p.classList.remove("on"));
    rebuildExecGrids();
    updateCompare();
  }

  function resetGpu() {
    if (gpuTimer) {
      clearInterval(gpuTimer);
      gpuTimer = null;
    }
    state.gpu = { wave: 0, elapsed: 0, playing: false, done: false, pcieDone: false };
    document.getElementById("gpu-wave").textContent = "0";
    document.getElementById("gpu-time-ms").textContent = "0 ms";
    document.getElementById("gpu-blocks-done").textContent = `0 / ${state.execBlocks}`;
    document.getElementById("pcie-indicator").classList.remove("active");
    document.getElementById("pcie-status-text").textContent = "Idle — host RAM holding the tensor";
    document.getElementById("gpu-note").textContent =
      "Run GPU to copy the tensor into VRAM, then watch parallel waves finish far fewer ticks than the CPU.";
    document.querySelectorAll("#gpu-sm-pills .core-pill").forEach((p) => p.classList.remove("on"));
    // only rebuild if cpu not mid-play labels — rebuildExecGrids clears both; call carefully
    for (let i = 0; i < state.execBlocks; i++) {
      const el = document.getElementById(`gpu-cell-${i}`);
      if (el) el.className = "tensor-cell";
    }
    updateCompare();
  }

  function cpuTickOnce() {
    const total = state.execBlocks;
    const cores = 4;
    if (state.cpu.idx >= total) {
      state.cpu.done = true;
      state.cpu.playing = false;
      if (cpuTimer) {
        clearInterval(cpuTimer);
        cpuTimer = null;
      }
      document.getElementById("cpu-play-btn").disabled = false;
      document.querySelectorAll("#cpu-core-pills .core-pill").forEach((p) => p.classList.remove("on"));
      const ticks = Math.ceil(total / cores);
      document.getElementById("cpu-note").innerHTML =
        `<strong>CPU finished:</strong> ${ticks} sequential ticks × 4 cores to cover ${total} blocks (${state.cpu.elapsed} ms simulated).`;
      state.checkpoints.cpu = true;
      updateProgress();
      updateCompare();
      return;
    }

    for (let i = 0; i < total; i++) {
      document.getElementById(`cpu-cell-${i}`).classList.remove("active-cpu");
    }
    document.querySelectorAll("#cpu-core-pills .core-pill").forEach((p) => p.classList.remove("on"));

    for (let c = 0; c < cores && state.cpu.idx < total; c++) {
      const i = state.cpu.idx;
      const cell = document.getElementById(`cpu-cell-${i}`);
      cell.classList.add("active-cpu", "done-cpu");
      document.querySelector(`#cpu-core-pills .core-pill[data-core="${c}"]`).classList.add("on");
      state.cpu.idx++;
    }
    state.cpu.tick++;
    state.cpu.elapsed += 80;
    document.getElementById("cpu-tick").textContent = String(state.cpu.tick);
    document.getElementById("cpu-blocks-done").textContent = `${state.cpu.idx} / ${total}`;
    document.getElementById("cpu-time-ms").textContent = `${state.cpu.elapsed} ms`;
  }

  document.getElementById("cpu-step-btn").addEventListener("click", () => {
    if (state.cpu.playing) return;
    if (state.cpu.done) resetCpu();
    cpuTickOnce();
  });

  document.getElementById("cpu-play-btn").addEventListener("click", () => {
    if (state.cpu.playing) return;
    if (state.cpu.done) resetCpu();
    state.cpu.playing = true;
    document.getElementById("cpu-play-btn").disabled = true;
    cpuTimer = setInterval(() => {
      cpuTickOnce();
      if (state.cpu.done) {
        clearInterval(cpuTimer);
        cpuTimer = null;
      }
    }, speedMs());
  });

  document.getElementById("cpu-reset-btn").addEventListener("click", resetCpu);

  function runGpu() {
    if (state.gpu.playing) return;
    if (state.gpu.done) {
      // soft reset gpu cells only
      state.gpu = { wave: 0, elapsed: 0, playing: false, done: false, pcieDone: false };
      for (let i = 0; i < state.execBlocks; i++) {
        document.getElementById(`gpu-cell-${i}`).className = "tensor-cell";
      }
      document.getElementById("gpu-wave").textContent = "0";
      document.getElementById("gpu-time-ms").textContent = "0 ms";
      document.getElementById("gpu-blocks-done").textContent = `0 / ${state.execBlocks}`;
    }

    state.gpu.playing = true;
    document.getElementById("gpu-play-btn").disabled = true;
    const pcie = document.getElementById("pcie-indicator");
    pcie.classList.add("active");
    document.getElementById("pcie-status-text").textContent =
      "Copying tensor blocks Host RAM → VRAM over PCIe…";

    // Short PCIe delay, then parallel waves
    setTimeout(() => {
      state.gpu.pcieDone = true;
      document.getElementById("pcie-status-text").textContent =
        "Tensor in VRAM — Streaming Multiprocessors launching parallel waves";
      const total = state.execBlocks;
      // Wave width: half the grid per wave (2 waves for 64, 2 waves for 256 also if we use 128)
      const blocksPerWave = Math.ceil(total / 2);
      let doneCount = 0;

      gpuTimer = setInterval(() => {
        for (let i = 0; i < total; i++) {
          document.getElementById(`gpu-cell-${i}`).classList.remove("active-gpu");
        }
        document.querySelectorAll("#gpu-sm-pills .core-pill").forEach((p) => p.classList.remove("on"));

        if (doneCount >= total) {
          clearInterval(gpuTimer);
          gpuTimer = null;
          state.gpu.playing = false;
          state.gpu.done = true;
          document.getElementById("gpu-play-btn").disabled = false;
          pcie.classList.remove("active");
          document.getElementById("pcie-status-text").textContent = "Transfer complete — compute finished in VRAM";
          document.getElementById("gpu-note").innerHTML =
            `<strong>GPU finished:</strong> 2 parallel waves after PCIe load (${state.gpu.elapsed} ms simulated) vs many sequential CPU ticks.`;
          state.checkpoints.gpu = true;
          updateProgress();
          updateCompare();
          return;
        }

        const start = doneCount;
        const end = Math.min(total, start + blocksPerWave);
        for (let i = start; i < end; i++) {
          const cell = document.getElementById(`gpu-cell-${i}`);
          cell.classList.add("active-gpu", "done-gpu");
        }
        document.querySelectorAll("#gpu-sm-pills .core-pill").forEach((p) => p.classList.add("on"));
        state.gpu.wave++;
        doneCount = end;
        state.gpu.elapsed += 45;
        document.getElementById("gpu-wave").textContent = String(state.gpu.wave);
        document.getElementById("gpu-blocks-done").textContent = `${doneCount} / ${total}`;
        document.getElementById("gpu-time-ms").textContent = `${state.gpu.elapsed} ms`;
      }, speedMs() + 40);
    }, Math.max(280, speedMs() * 2));
  }

  document.getElementById("gpu-play-btn").addEventListener("click", runGpu);
  document.getElementById("gpu-reset-btn").addEventListener("click", () => {
    resetGpu();
    rebuildExecGrids();
    // restore cpu progress visually if any
    if (state.cpu.idx > 0) {
      for (let i = 0; i < state.cpu.idx; i++) {
        document.getElementById(`cpu-cell-${i}`).classList.add("done-cpu");
      }
      document.getElementById("cpu-tick").textContent = String(state.cpu.tick);
      document.getElementById("cpu-blocks-done").textContent = `${state.cpu.idx} / ${state.execBlocks}`;
      document.getElementById("cpu-time-ms").textContent = `${state.cpu.elapsed} ms`;
    }
  });

  document.querySelectorAll("#exec-size-buttons .pill-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#exec-size-buttons .pill-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.execBlocks = Number(btn.dataset.blocks);
      resetCpu();
      resetGpu();
      rebuildExecGrids();
    });
  });

  function updateCompare() {
    const bar = document.getElementById("compare-bar");
    if (state.cpu.done && state.gpu.done) {
      const ratio = (state.cpu.elapsed / Math.max(1, state.gpu.elapsed)).toFixed(1);
      bar.classList.add("ready");
      bar.innerHTML =
        `<strong>Compare:</strong> CPU ${state.cpu.elapsed} ms vs GPU ${state.gpu.elapsed} ms ` +
        `(~${ratio}× faster on this grid). Same math — different parallelism. Scroll to Stage 4 for KodeFood scale-up.`;
      updateScale(Number(document.getElementById("scale-slider").value));
    } else {
      bar.classList.remove("ready");
      bar.innerHTML =
        "<strong>Compare:</strong> Finish both runs to unlock the timing ratio and Stage 4 scale-up insight.";
    }
  }

  // ---- Stage 4: scale ----
  const SCALE = [
    {
      label: "1 photo",
      cpuMs: 1280,
      gpuMs: 90,
      cpuBar: 12,
      gpuBar: 4,
      summary:
        "One dish tensor: the CPU walks the grid carefully; the GPU sweeps it in parallel waves. The gap is already visible.",
      takeaway:
        "Even a single caption pass prefers the GPU for dense multiply-and-add across patches.",
    },
    {
      label: "30 photos (1 vendor folder)",
      cpuMs: 38400,
      gpuMs: 2700,
      cpuBar: 45,
      gpuBar: 10,
      summary:
        "One KodeFood vendor folder (~30 photos). Sequential CPU time stretches into tens of seconds; a GPU finishes the folder in a short burst.",
      takeaway:
        "This is the shape AWS Batch loves: finite work, GPU for the math, then release capacity.",
    },
    {
      label: "3,000 photos (100 vendors)",
      cpuMs: 3840000,
      gpuMs: 270000,
      cpuBar: 100,
      gpuBar: 28,
      summary:
        "At marketplace scale, CPU backlog becomes hours while GPU bursts stay in the minutes — then Spot/Batch can scale toward zero when the queue drains.",
      takeaway:
        "Cloud takeaway: rent a GPU for the short burst, write descriptions.csv, then scale toward zero.",
    },
  ];

  function formatMs(ms) {
    if (ms < 1000) return `${ms} ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)} s`;
    return `${(ms / 60000).toFixed(1)} min`;
  }

  function updateScale(idx) {
    const s = SCALE[idx];
    document.getElementById("scale-summary").textContent = s.summary;
    document.getElementById("cpu-scale-time").textContent = formatMs(s.cpuMs);
    document.getElementById("gpu-scale-time").textContent = formatMs(s.gpuMs);
    document.getElementById("cpu-scale-bar").style.width = `${s.cpuBar}%`;
    document.getElementById("gpu-scale-bar").style.width = `${s.gpuBar}%`;
    document.getElementById("scale-takeaway").textContent = s.takeaway;
  }

  document.getElementById("scale-slider").addEventListener("input", (e) => {
    updateScale(Number(e.target.value));
  });

  document.getElementById("reset-all-btn").addEventListener("click", () => {
    window.location.reload();
  });

  // Init
  resetPixels(8);
  updateScale(0);
  updateProgress();
})();
