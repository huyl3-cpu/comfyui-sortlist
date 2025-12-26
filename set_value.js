import { app } from "../../scripts/app.js";

/**
 * UI-only extension for "Set Value"
 * - KHÔNG rewrite prompt
 * - KHÔNG patch queuePrompt/fetch
 * - Không còn mask_text
 */
app.registerExtension({
  name: "vf9.SetValue.uiOnly",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    const n = nodeData?.name;
    if (n !== "Set Value" && n !== "VF9_SetValue") return;

    const origCreated = nodeType.prototype.onNodeCreated;
    const origConn = nodeType.prototype.onConnectionsChange;

    function refresh(node) {
      try { node.setSize(node.computeSize()); } catch (e) {}
      node.setDirtyCanvas(true, true);
    }

    nodeType.prototype.onNodeCreated = function () {
      if (origCreated) origCreated.apply(this, arguments);
      refresh(this);
    };

    nodeType.prototype.onConnectionsChange = function () {
      if (origConn) origConn.apply(this, arguments);
      refresh(this);
    };
  },
});
