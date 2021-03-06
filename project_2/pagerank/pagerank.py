from decimal import Decimal
import os
import random
import re
import sys

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
    probability_distribution = dict()
    corpus_size = len(corpus)
    links_number = len(corpus[page])
    if links_number == 0:
        damping_factor = 0
    for elem in corpus:
        value = (Decimal('1') - Decimal(f'{damping_factor}')) / corpus_size
        if elem in corpus[page]:
            value += Decimal(f'{damping_factor}') / links_number
        probability_distribution[elem] = float(value)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {key: 0 for key in corpus}

    # Choose first page at random
    current_page = random.choice(list(corpus))
    page_rank[current_page] = 1

    # Continue until n samples are generated
    i = 1
    while i < n:
        prob_distribution = transition_model(corpus, current_page,
                                             damping_factor)
        current_page = random.choices(list(prob_distribution),
                                      weights=list(prob_distribution.values()),
                                      k=1)[0]
        page_rank[current_page] += 1
        i += 1

    # Calculate PageRank values
    for key in page_rank:
        page_rank[key] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Calculate initial PageRank values
    corpus_size = len(corpus)
    page_rank = {key: 1 / corpus_size for key in corpus}

    # Replace values for pages that have no links at all
    edited_corpus = no_links_page(corpus)

    # Get dict mapping page with set of all pages that link to it
    links_to_pages = links_to_page(edited_corpus)

    # Continue to calculate new PageRank values
    while True:
        result = dict()
        for page in page_rank:
            pr = (1 - damping_factor) / corpus_size
            link_sum = 0
            for el in links_to_pages[page]:
                link_sum += page_rank[el] / len(edited_corpus[el])
            pr += damping_factor * link_sum
            result[page] = pr

        # Break if no PageRank value changes by more than 0.001
        # since the last iteration
        if all([abs(page_rank[p] - result[p]) <= 0.001 for p in page_rank]):
            break

        # Save the last iteration results
        page_rank = result

    return result


def no_links_page(corpus):
    """
    Return edited corpus dictionary where all pages that had no
    links at all now have one link to every page in the corpus.
    """
    return {key: (v if v else set(corpus)) for key, v in corpus.items()}


def links_to_page(corpus):
    """
    Return dictionary mapping page name to a set of all pages
    possessing link to that page.
    """
    result = dict()
    for page in corpus:
        links = set()
        for key in corpus:
            if page in corpus[key]:
                links.add(key)
        result[page] = links

    return result


if __name__ == "__main__":
    main()
