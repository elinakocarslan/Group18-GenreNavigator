

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.DB2CvQJj.js","_app/immutable/chunks/disclose-version.BFHv33CP.js","_app/immutable/chunks/runtime.Bh6GFcG-.js"];
export const stylesheets = [];
export const fonts = [];
