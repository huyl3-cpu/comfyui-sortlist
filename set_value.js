import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

/** Allow OPT_CONNECTION to connect to any type (like rgthree) */
function patchOptConnectionCompatibility() {
  const LG = globalThis.LiteGraph;
  if (!LG) return;
  if (LG.__vf9_optconnection_patched) return;
  LG.__vf9_optconnection_patched = true;

  const orig = LG.isValidConnection;
  LG.isValidConnection = function (a, b) {
    if (a === "OPT_CONNECTION" || b === "OPT_CONNECTION") return true;
    if (!a || !b || a === "*" || b === "*") return true;
    return orig ? orig.call(this, a, b) : true;
  };

  console.log("[vf9] Patched LiteGraph.isValidConnection for OPT_CONNECTION");
}

function getKeyCI(obj, name) {
  if (!obj) return undefined;
  if (obj[name] !== undefined) return obj[name];
  const low = name.toLowerCase();
  for (const k of Object.keys(obj)) {
    if (k.toLowerCase() === low) return obj[k];
  }
  return undefined;
}

function truthyBool(v, defaultVal = true) {
  if (v === undefined) return defaultVal;
  if (v === false) return false;
  // accept "false"/"0" as false
  if (typeof v === "string") {
    const s = v.trim().toLowerCase();
    if (s === "false" || s === "0" || s === "no") return false;
    return true;
  }
  return !!v;
}

/** Rewrite prompt: remove Set Value and rewire its outputs */
function rewriteSetValuePrompt(prompt) {
  if (!prompt || typeof prompt !== "object") return;

  const ids = Object.keys(prompt).filter((id) => prompt[id]?.class_type === "Set Value");
  if (!ids.length) return;

  const replaceRefs = (fromId, outIndex, replacement) => {
    for (const nid of Object.keys(prompt)) {
      if (nid === fromId) continue;
      const inputs = prompt[nid]?.inputs;
      if (!inputs) continue;

      for (const k of Object.keys(inputs)) {
        const v = inputs[k];

        // Replace only if it references our Set Value output
        if (Array.isArray(v) && String(v[0]) === String(fromId) && v[1] === outIndex) {
          if (replacement === null) delete inputs[k];
          else inputs[k] = replacement;
        }
      }

      // Safety: never leave null in inputs (can crash nodes like SaveImage)
      for (const k of Object.keys(inputs)) {
        if (inputs[k] === null) delete inputs[k];
      }
    }
  };

  for (const sid of ids) {
    const inp = prompt[sid]?.inputs || {};

    // case-insensitive enables
    const enBg = truthyBool(getKeyCI(inp, "enable_background"), true);
    const enFace = truthyBool(getKeyCI(inp, "enable_face"), true);
    const enMask = truthyBool(getKeyCI(inp, "enable_mask"), true);

    // case-insensitive sources
    const srcBg = getKeyCI(inp, "background");
    const srcFace = getKeyCI(inp, "face");
    const srcMask = getKeyCI(inp, "mask");

    // output indices (must match value.py RETURN_NAMES):
    // 0 background, 1 face, 2 mask, 3 mask_text
    if (enBg && Array.isArray(srcBg)) replaceRefs(sid, 0, srcBg);
    else replaceRefs(sid, 0, null);

    if (enFace && Array.isArray(srcFace)) replaceRefs(sid, 1, srcFace);
    else replaceRefs(sid, 1, null);

    if (enMask && Array.isArray(srcMask)) replaceRefs(sid, 2, srcMask);
    else replaceRefs(sid, 2, null);

    // mask_text literal string if enable_mask true
    if (enMask) {
      const textVal = String(getKeyCI(inp, "mask_text") ?? "");
      replaceRefs(sid, 3, textVal);
    } else {
      replaceRefs(sid, 3, null);
    }

    delete prompt[sid];
  }
}

function rewriteInPayload(payload) {
  if (!payload || typeof payload !== "object") return;
  if (payload.prompt && typeof payload.prompt === "object") rewriteSetValuePrompt(payload.prompt);
  else if (payload && typeof payload === "object") rewriteSetValuePrompt(payload);
}

app.registerExtension({
  name: "vf9.SetValue.forceRewrite",

  async setup() {
    patchOptConnectionCompatibility();

    // Patch api.queuePrompt (reliable)
    if (api?.queuePrompt && !api.__vf9_queuePrompt_patched) {
      api.__vf9_queuePrompt_patched = true;
      const orig = api.queuePrompt.bind(api);
      api.queuePrompt = async function (payload, ...rest) {
        try { rewriteInPayload(payload); } catch (e) {}
        return await orig(payload, ...rest);
      };
      console.log("[vf9] Patched api.queuePrompt");
    }

    // Fallback: intercept fetch POST /prompt
    if (!globalThis.__vf9_fetch_patched) {
      globalThis.__vf9_fetch_patched = true;
      const origFetch = globalThis.fetch.bind(globalThis);

      globalThis.fetch = async function (input, init) {
        try {
          const url = typeof input === "string" ? input : input?.url || "";
          const method = (init?.method || "GET").toUpperCase();
          if (method === "POST" && url.includes("/prompt") && init?.body && typeof init.body === "string") {
            const parsed = JSON.parse(init.body);
            rewriteInPayload(parsed);
            init = { ...init, body: JSON.stringify(parsed) };
          }
        } catch (e) {}
        return await origFetch(input, init);
      };

      console.log("[vf9] Patched fetch(/prompt) fallback");
    }

    console.log("[vf9] Set Value loaded (case-insensitive rewrite)");
  },
});
