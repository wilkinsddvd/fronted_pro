import { marked } from 'marked'
import hljs from 'highlight.js'

export function renderMarkdown(md) {
  return marked.parse(md, {
    highlight: code => hljs.highlightAuto(code).value
  })
}