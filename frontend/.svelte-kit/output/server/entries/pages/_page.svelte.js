import { e as escape_html } from "../../chunks/escaping.js";
import { S as pop, Q as push } from "../../chunks/index.js";
const replacements = {
  translate: /* @__PURE__ */ new Map([
    [true, "yes"],
    [false, "no"]
  ])
};
function attr(name, value, is_boolean = false) {
  if (is_boolean || name === "class") return "";
  const normalized = name in replacements && replacements[name].get(value) || value;
  const assignment = is_boolean ? "" : `="${escape_html(normalized, true)}"`;
  return ` ${name}${assignment}`;
}
function _page($$payload, $$props) {
  push();
  let targetWord = "";
  let synonyms = [];
  let guess = "";
  let similarity = 0;
  let message = "";
  $$payload.out += `<main class="svelte-6qjbxb"><h1>Contexto Game</h1> <p>Try to guess the target word!</p> <p>Hint: The target word has ${escape_html(targetWord.length)} letters.</p> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> `;
  if (synonyms.length > 0) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<p><strong>Synonyms (hidden for now):</strong> ${escape_html(synonyms.length)} synonyms available.</p>`;
  } else {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> <input type="text"${attr("value", guess)} placeholder="Enter your guess" class="svelte-6qjbxb"> <button class="svelte-6qjbxb">Submit Guess</button> <p>${escape_html(message)}</p> <p>Similarity Score: ${escape_html(similarity)}</p></main>`;
  pop();
}
export {
  _page as default
};
