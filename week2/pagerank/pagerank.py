import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    new_dict = {}
    for link in corpus:
        new_dict[link]= None

    if len(corpus[page])== 0:
        for link in new_dict:
            new_dict[link]=1/len(corpus)
        return new_dict

    for link in new_dict:
        new_dict[link]= (1-damping_factor)/len(corpus)
        if link != page and link in corpus[page]:
            new_dict[link] += damping_factor*(1/len(corpus[page]))
    return new_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    new_dict = {}
    for link in corpus:
        new_dict[link]= 0

    pages= list(corpus.keys())
    pagei = random.choice(pages)
    new_dict[random.choice(list(corpus.keys()))] = 1

    for i in range(n-1):
        d= transition_model(corpus,pagei,damping_factor)
        pages= list(d.keys())
        weight= list(d.values())
        pagei = random.choices(pages,weight,k=1)[0]
        new_dict[pagei]+= 1
    
    for link in new_dict:
        new_dict[link]= new_dict[link]/n

    return new_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_links = len(corpus)
    d = damping_factor
    new_dict = {}
    
    for link in corpus:
        new_dict[link]= 1/num_links
        
    # Método iterativo
    while True:
        # Cria uma cópia para comparar o erro
        copia = copy.deepcopy(new_dict)
        erro = 0

        # Calcula a nova PR para cada link 
        for link in new_dict:
            var_value = 0
            # Somatório PR(i)/Numlinks(i)
            for i in corpus:
                if i != link and link in corpus[i]:
                    var_value += new_dict[i]/len(corpus[i])

            # Atualiza o PR do link em questão
            new_dict[link] = ((1-d)/num_links) + d*var_value
        
        # Falta só comparar o erro, o erro máximo precisa ser de 0.001
        for link in new_dict:
            erro=  max(abs(new_dict[link]-copia[link]),erro)
            
        if erro < 0.001 or erro> 1:
            return new_dict


if __name__ == "__main__":
    main()
