// 简单提取markdown中的yaml front-matter (适合小型自用博客)
export function parseFrontMatter(mdContent) {
  const match = mdContent.match(/^---\n([\s\S]+?)\n---\n([\s\S]*)$/)
  if (!match) return { meta: {}, content: mdContent }
  const meta = {}
  match[1].split('\n').forEach(line => {
    const [key, ...rest] = line.split(':')
    meta[key.trim()] = rest.join(':').trim()
  })
  return { meta, content: match[2] }
}