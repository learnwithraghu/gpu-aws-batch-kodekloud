(function () {
  "use strict";

  const state = {
    blocks: 64,
    cpu: { idx: 0, tick: 0, elapsed: 0, playing: false, done: false },
    gpu: { wave: 0, doneCount: 0, elapsed: 0, playing: false, done: false },
  };

  let cpuTimer = null;
  let gpuTimer = null;

  const cpuGrid = document.getElementById("cpu-grid");
  const gpuGrid = document.getElementById("gpu-grid");

  function speedMs() {
    const v = document.getElementById("speed-select").value;
    if (v === "slow") return 220;
    if (v === "fast") return 55;
    return 110;
  }

  function rebuildGrids() {
    const n = state.blocks;
    const cols = Math.sqrt(n);
    cpuGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    gpuGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    cpuGrid.innerHTML = "";
    gpuGrid.innerHTML = "";
    for (let i = 0; i < n; i++) {
      const c = document.createElement("div");
      c.className = "tensor-cell";
      c.id = `cpu-cell-${i}`;
      cpuGrid.appendChild(c);
      const g = document.createElement("div");
      g.className = "tensor-cell";
      g.id = `gpu-cell-${i}`;
      gpuGrid.appendChild(g);
    }
    document.getElementById("cpu-done").textContent = `0 / ${n}`;
    document.getElementById("gpu-done").textContent = `0 / ${n}`;
  }

  function clearCpuVisual() {
    for (let i = 0; i < state.blocks; i++) {
      const el = document.getElementById(`cpu-cell-${i}`);
      if (el) el.className = "tensor-cell";
    }
    document.querySelectorAll("#cpu-cores .core-pill").forEach((p) => p.classList.remove("on"));
  }

  function clearGpuVisual() {
    for (let i = 0; i < state.blocks; i++) {
      const el = document.getElementById(`gpu-cell-${i}`);
      if (el) el.className = "tensor-cell";
    }
    document.querySelectorAll("#gpu-sms .core-pill").forEach((p) => p.classList.remove("on"));
  }

  function resetCpu(keepGrid) {
    if (cpuTimer) {
      clearInterval(cpuTimer);
      cpuTimer = null;
    }
    state.cpu = { idx: 0, tick: 0, elapsed: 0, playing: false, done: false };
    document.getElementById("cpu-tick").textContent = "0";
    document.getElementById("cpu-time").textContent = "0 ms";
    document.getElementById("cpu-done").textContent = `0 / ${state.blocks}`;
    document.getElementById("cpu-play-btn").disabled = false;
    document.getElementById("cpu-note").innerHTML =
      "Click <strong>Step</strong> to march 4 cores across the grid, or <strong>Play CPU</strong> for the full sequential run.";
    if (!keepGrid) clearCpuVisual();
    else {
      clearCpuVisual();
    }
    updateCompare();
  }

  function resetGpu() {
    if (gpuTimer) {
      clearInterval(gpuTimer);
      gpuTimer = null;
    }
    state.gpu = { wave: 0, doneCount: 0, elapsed: 0, playing: false, done: false };
    document.getElementById("gpu-wave").textContent = "0";
    document.getElementById("gpu-time").textContent = "0 ms";
    document.getElementById("gpu-done").textContent = `0 / ${state.blocks}`;
    document.getElementById("gpu-play-btn").disabled = false;
    document.getElementById("gpu-note").innerHTML =
      "Click <strong>Play GPU</strong> to watch parallel Streaming Multiprocessors finish the same blocks in a few wide waves.";
    clearGpuVisual();
    updateCompare();
  }

  function resetAll() {
    resetCpu();
    resetGpu();
    rebuildGrids();
    document.getElementById("done-banner").classList.add("hidden");
    document.getElementById("progress-pill").textContent = "Run both sides to compare";
    document.getElementById("progress-pill").classList.remove("done");
  }

  function cpuTickOnce() {
    const total = state.blocks;
    const cores = 4;

    if (state.cpu.idx >= total) {
      state.cpu.done = true;
      state.cpu.playing = false;
      if (cpuTimer) {
        clearInterval(cpuTimer);
        cpuTimer = null;
      }
      document.getElementById("cpu-play-btn").disabled = false;
      document.querySelectorAll("#cpu-cores .core-pill").forEach((p) => p.classList.remove("on"));
      const ticks = Math.ceil(total / cores);
      document.getElementById("cpu-note").innerHTML =
        `<strong>CPU finished:</strong> ${ticks} sequential ticks × 4 cores to cover ${total} blocks (${state.cpu.elapsed} ms).`;
      updateCompare();
      return;
    }

    for (let i = 0; i < total; i++) {
      document.getElementById(`cpu-cell-${i}`).classList.remove("active-cpu");
    }
    document.querySelectorAll("#cpu-cores .core-pill").forEach((p) => p.classList.remove("on"));

    for (let c = 0; c < cores && state.cpu.idx < total; c++) {
      const i = state.cpu.idx;
      const cell = document.getElementById(`cpu-cell-${i}`);
      cell.classList.add("active-cpu", "done-cpu");
      document.querySelector(`#cpu-cores .core-pill[data-core="${c}"]`).classList.add("on");
      state.cpu.idx++;
    }

    state.cpu.tick++;
    state.cpu.elapsed += 80;
    document.getElementById("cpu-tick").textContent = String(state.cpu.tick);
    document.getElementById("cpu-done").textContent = `${state.cpu.idx} / ${total}`;
    document.getElementById("cpu-time").textContent = `${state.cpu.elapsed} ms`;
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

  function runGpu() {
    if (state.gpu.playing) return;
    if (state.gpu.done) resetGpu();

    state.gpu.playing = true;
    document.getElementById("gpu-play-btn").disabled = true;

    const total = state.blocks;
    const blocksPerWave = Math.ceil(total / 2);

    gpuTimer = setInterval(() => {
      for (let i = 0; i < total; i++) {
        document.getElementById(`gpu-cell-${i}`).classList.remove("active-gpu");
      }
      document.querySelectorAll("#gpu-sms .core-pill").forEach((p) => p.classList.remove("on"));

      if (state.gpu.doneCount >= total) {
        clearInterval(gpuTimer);
        gpuTimer = null;
        state.gpu.playing = false;
        state.gpu.done = true;
        document.getElementById("gpu-play-btn").disabled = false;
        document.getElementById("gpu-note").innerHTML =
          `<strong>GPU finished:</strong> ${state.gpu.wave} parallel waves covered ${total} blocks (${state.gpu.elapsed} ms).`;
        updateCompare();
        return;
      }

      const start = state.gpu.doneCount;
      const end = Math.min(total, start + blocksPerWave);
      for (let i = start; i < end; i++) {
        document.getElementById(`gpu-cell-${i}`).classList.add("active-gpu", "done-gpu");
      }
      document.querySelectorAll("#gpu-sms .core-pill").forEach((p) => p.classList.add("on"));

      state.gpu.wave++;
      state.gpu.doneCount = end;
      state.gpu.elapsed += 45;
      document.getElementById("gpu-wave").textContent = String(state.gpu.wave);
      document.getElementById("gpu-done").textContent = `${state.gpu.doneCount} / ${total}`;
      document.getElementById("gpu-time").textContent = `${state.gpu.elapsed} ms`;
    }, speedMs() + 30);
  }

  document.getElementById("gpu-play-btn").addEventListener("click", runGpu);

  function updateCompare() {
    const bar = document.getElementById("compare-bar");
    const pill = document.getElementById("progress-pill");
    const banner = document.getElementById("done-banner");

    if (state.cpu.done && state.gpu.done) {
      const ratio = (state.cpu.elapsed / Math.max(1, state.gpu.elapsed)).toFixed(1);
      bar.classList.add("ready");
      bar.innerHTML =
        `<strong>Result:</strong> CPU ${state.cpu.elapsed} ms vs GPU ${state.gpu.elapsed} ms ` +
        `(~${ratio}× faster on this grid). Same math — sequential cores vs parallel waves.`;
      pill.textContent = "Comparison complete";
      pill.classList.add("done");
      document.getElementById("done-text").textContent =
        `CPU needed ${state.cpu.tick} sequential ticks. GPU finished in ${state.gpu.wave} parallel waves ` +
        `(~${ratio}× faster here). That is why KodeFood caption math belongs on a GPU.`;
      banner.classList.remove("hidden");
    } else {
      bar.classList.remove("ready");
      bar.innerHTML =
        "Finish <strong>Play CPU</strong> and <strong>Play GPU</strong> on the same grid size to unlock the timing comparison.";
      pill.textContent = "Run both sides to compare";
      pill.classList.remove("done");
      banner.classList.add("hidden");
    }
  }

  document.querySelectorAll("#size-buttons .pill-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#size-buttons .pill-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.blocks = Number(btn.dataset.blocks);
      resetAll();
    });
  });

  document.getElementById("reset-btn").addEventListener("click", resetAll);

  rebuildGrids();
  updateCompare();
})();
