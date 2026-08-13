from ddgs import DDGS
import subprocess, re, json

def fetch(url, timeout=20):
    try:
        r = subprocess.run(['curl', '-sL', '--max-time', str(timeout), '-A', 'Mozilla/5.0', url], capture_output=True, text=True, timeout=timeout+5)
        text = r.stdout
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:3500]
    except Exception as e:
        return f"ERR: {e}"

queries = [
    '"elsarticle" frontmatter order title author affiliation abstract keywords MSC',
    '"tectonic" GitHub Actions "wget" OR "curl" binary install',
    'elsarticle "review" mode keyword not supported',
    'texlive/texlive docker "elsarticle" publishers',
    'latex CI validate tex files lacheck chktex',
    'arxiv texlive docker compile reproducible',
]
for q in queries:
    print(f'\n=== {q} ===')
    with DDGS() as ddgs:
        results = list(ddgs.text(q, max_results=5))
        for r in results:
            print(f"  [{r.get('href','')[:80]}] {r.get('title','')[:90]}")
