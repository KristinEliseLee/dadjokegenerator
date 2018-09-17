import requests
from random import choice

# Due to unicode characters in the dataset that couldn't map to charmap, I had
# to encode all the text files as utf-8 

def get_all_jokes(save='all_jokes.txt'):
    """Gets all jokes from icanhasdadjoke.com, saves to text file.
    Also removes any new lines from inside of jokes, and ends each joke with a 
    | character and a new line, to deal with a few specifically formatted jokes.

    This should only be called to initialize the joke repository as making this 
    call every time adds a lot of time to generating the joke.


    Below doctests relies on the current first joke listed online not changing.
    If it changes, doctest will need to be updates

    >>> get_all_jokes()
    >>> source = open('all_jokes.txt', 'r', encoding='utf-8')
    >>> r = source.readlines()
    >>> source.close()
    >>> "I'm tired" in r[0]
    True


    """
    with open(save,'w+',encoding='utf-8') as all_jokes:
        jokes = requests.get('https://icanhazdadjoke.com/search',
            headers={'Accept':'application/json'})
        jokes_info = jokes.json()
        num_pages = jokes_info['total_pages']
        for i in range(1, num_pages+1):
            params = {'page': i}
            joke_page = requests.get('https://icanhazdadjoke.com/search',
                headers={'Accept':'application/json'}, params=params)
            joke_page = joke_page.json()
        
            for joke in joke_page['results']:
                joke_text = joke['joke'].replace('\r', '')
                joke_text = joke_text.replace('\n', '')
                all_jokes.write(joke_text + '|\n')

def generate_markov_dict(keylen, source):
    """ Returns a dictionary with tuples of keylen length, and a starting tuples list
    keylen is how long each key is, it controls how much sense the joke will
    probably make.

    source is the source text file

    first joke listed online is 'I'm tired of following my dreams. I'm just going 
    to ask them where they are going and meet up with them later.'

    if the joke repository changes, this doctest will need to be updated.

    >>> get_all_jokes()
    >>> joke_dict, joke_starts = generate_markov_dict(2, 'all_jokes.txt')
    >>> ("I'm", "tired") in joke_starts
    True
    >>> 'of' in joke_dict[("I'm", "tired")]
    True


    """


    joke_dict= {}
    joke_starts=[]

    with open(source,'r', encoding='utf-8') as originals:
        for line in originals.readlines():
            words=line.split()
            for i in range(len(words) - (keylen)):
                key = tuple(words[i:i+keylen])
                if i == 0:
                    joke_starts.append(key)
                joke_dict.setdefault(key, []).append(words[i+keylen])

    return (joke_dict, joke_starts)

def make_joke(keylen=2, save='save.txt', source='all_jokes.txt'):
    """Creates a joke and appends it to save file, returns the joke

    For below doctests, as this is a random text generator, I could only test
    that it did create a string. The length and content of the string will
    naturally depend on the outcomes of random.choice.

    Also note that some jokes have unicode characters in them (mostly fancy quote marks)
    so they might have blocks when displayed in the console

    >>> get_all_jokes()
    >>> joke = make_joke()
    >>> type(joke) == str
    True
    >>> len(joke) > 5
    True

    """
    joke_dict, joke_starts = generate_markov_dict(keylen, source)
    joke_list = []
    start = choice(joke_starts)
    joke_list.extend(start)


    while joke_list[-1][-1] != '|' and len(joke_list) <200:
        key = tuple(joke_list[keylen*-1:])
        joke_list.append(choice(joke_dict[key]))

    joke_list[-1]=joke_list[-1].replace('|','')
    joke = ' '.join(joke_list)

    with open(save, 'a', encoding='utf-8') as save_file:
        save_file.write(joke + '\n')

    return joke


get_all_jokes() # only necessary to do the first time
joke = make_joke()
print(joke)
