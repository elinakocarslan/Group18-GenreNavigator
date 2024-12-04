export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.DyLdx4P9.js","app":"_app/immutable/entry/app.Sk1EAklm.js","imports":["_app/immutable/entry/start.DyLdx4P9.js","_app/immutable/chunks/entry.EgGmjmqu.js","_app/immutable/chunks/runtime.Bh6GFcG-.js","_app/immutable/entry/app.Sk1EAklm.js","_app/immutable/chunks/runtime.Bh6GFcG-.js","_app/immutable/chunks/render.DWMY3bxJ.js","_app/immutable/chunks/disclose-version.BFHv33CP.js","_app/immutable/chunks/index-client.DfNTHW60.js","_app/immutable/chunks/store.CsM_bYrq.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
