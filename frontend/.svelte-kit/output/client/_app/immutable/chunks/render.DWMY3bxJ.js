import{S as E,U as b,V,Q as O,i as q,W as C,X as H,Y as M,Z as L,P as $,_ as B,$ as j,a0 as T,G as w,F as A,C as F,c as p,a1 as G,a2 as Q,a3 as U,a4 as X,a5 as Z,a6 as z,O as J,a as K,p as x,h as S,e as ee,q as te}from"./runtime.Bh6GFcG-.js";import{b as re}from"./disclose-version.BFHv33CP.js";let D=!1;function ae(){D||(D=!0,document.addEventListener("reset",e=>{Promise.resolve().then(()=>{var t;if(!e.defaultPrevented)for(const a of e.target.elements)(t=a.__on_r)==null||t.call(a)})},{capture:!0}))}function k(e){var t=V,a=O;E(null),b(null);try{return e()}finally{E(t),b(a)}}function le(e,t,a,i=a){e.addEventListener(t,()=>k(a));const n=e.__on_r;n?e.__on_r=()=>{n(),i()}:e.__on_r=i,ae()}const ne=new Set,P=new Set;function se(e,t,a,i){function n(r){if(i.capture||y.call(t,r),!r.cancelBubble)return k(()=>a.call(this,r))}return e.startsWith("pointer")||e.startsWith("touch")||e==="wheel"?C(()=>{t.addEventListener(e,n,i)}):t.addEventListener(e,n,i),n}function _e(e,t,a,i,n){var r={capture:i,passive:n},u=se(e,t,a,r);(t===document.body||t===window||t===document)&&q(()=>{t.removeEventListener(e,u,r)})}function y(e){var R;var t=this,a=t.ownerDocument,i=e.type,n=((R=e.composedPath)==null?void 0:R.call(e))||[],r=n[0]||e.target,u=0,h=e.__root;if(h){var l=n.indexOf(h);if(l!==-1&&(t===document||t===window)){e.__root=t;return}var _=n.indexOf(t);if(_===-1)return;l<=_&&(u=l)}if(r=n[u]||e.target,r!==t){H(e,"currentTarget",{configurable:!0,get(){return r||a}});var m=V,f=O;E(null),b(null);try{for(var s,o=[];r!==null;){var c=r.assignedSlot||r.parentNode||r.host||null;try{var d=r["__"+i];if(d!==void 0&&!r.disabled)if(M(d)){var[W,...Y]=d;W.apply(r,[e,...Y])}else d.call(r,e)}catch(g){s?o.push(g):s=g}if(e.cancelBubble||c===t||c===null)break;r=c}if(s){for(let g of o)queueMicrotask(()=>{throw g});throw s}}finally{e.__root=t,delete e.currentTarget,E(m),b(f)}}}const ie=["touchstart","touchmove"];function oe(e){return ie.includes(e)}function de(e,t){var a=t==null?"":typeof t=="object"?t+"":t;a!==(e.__t??(e.__t=e.nodeValue))&&(e.__t=a,e.nodeValue=a==null?"":a+"")}function ue(e,t){return I(e,t)}function he(e,t){L(),t.intro=t.intro??!1;const a=t.target,i=S,n=p;try{for(var r=$(a);r&&(r.nodeType!==8||r.data!==B);)r=j(r);if(!r)throw T;w(!0),A(r),F();const u=I(e,{...t,anchor:r});if(p===null||p.nodeType!==8||p.data!==G)throw Q(),T;return w(!1),u}catch(u){if(u===T)return t.recover===!1&&U(),L(),X(a),w(!1),ue(e,t);throw u}finally{w(i),A(n)}}const v=new Map;function I(e,{target:t,anchor:a,props:i={},events:n,context:r,intro:u=!0}){L();var h=new Set,l=f=>{for(var s=0;s<f.length;s++){var o=f[s];if(!h.has(o)){h.add(o);var c=oe(o);t.addEventListener(o,y,{passive:c});var d=v.get(o);d===void 0?(document.addEventListener(o,y,{passive:c}),v.set(o,1)):v.set(o,d+1)}}};l(Z(ne)),P.add(l);var _=void 0,m=z(()=>{var f=a??t.appendChild(J());return K(()=>{if(r){x({});var s=te;s.c=r}n&&(i.$$events=n),S&&re(f,null),_=e(f,i)||{},S&&(O.nodes_end=p),r&&ee()}),()=>{var c;for(var s of h){t.removeEventListener(s,y);var o=v.get(s);--o===0?(document.removeEventListener(s,y),v.delete(s)):v.set(s,o)}P.delete(l),N.delete(_),f!==a&&((c=f.parentNode)==null||c.removeChild(f))}});return N.set(_,m),_}let N=new WeakMap;function ve(e){const t=N.get(e);t&&t()}export{ae as a,_e as e,he as h,le as l,ue as m,de as s,ve as u};