# wordle-solver
A solver for wordle type games. It works by picking the word that minimises the maximum possible size of the set of remaining words in the next step. In other words, it minimises the size of the worst-case scenario.

There is a second mode that instead minimises the average size of the set of remaining words. This is especially useful when multiple words give the same worst-case set size, as it gives a way to evaluate which option is best.

## Word lists
Wordle uses two lists, here called `wordle.txt` and `wordleAnswers.txt`. The first is the list of all words wordle considers valid when making guesses, and so this is the list of words that the program will suggest as guesses. `wordleAnswers.txt` on the other hand is the list of words that wordle will use as answers, and is a smaller list excluding a lot of obscure words. This is fairly typical in wordle type games, and in this case both lists can be extracted from the wordle webpage with some help of the browser's dev tools.

For the case of nerdle, things are a little trickier. I was unable to extract the two lists from the webpage, but there is enough information given at https://faqs.nerdlegame.com/?faq to recreate both. The script `nerdle.py` does exactly this, with the `produce` function producing 169199 valid guesses, and the function `reduce` reduces this to 17724 valid answers. Note that `produce` takes a minute or so to process. On the page above, it says there are "over 100,000 valid words", and exactly 17723 ideal words they use as answers. Interestingly, the `reduce` function misses the edge case "000000=0", which accounts for the difference. I could of course fix this but I think it is funny.

## Usage
Using the `Solve` functions allows the user to pass in a specific answer and see what guesses the selected algorithm would choose in solving it. To solve an unseen example requires more work, and requires directly interfacing with the `table` function. Without any arguments, this function searches all possible guesses for the best opening. 

Suppose that you've tried the words `hello` and `crane`, and now have two results to feed in. First, the results are converted to an array, where green is 2, orange is 1, and grey is 0. This gives something like `rel = [2,1,2,0,0, 1,2,0,0,0]`, where the first 5 are the output from `hello` and the second 5 are from `crane` This is done by calling `table( fw = ['hello','crane'], fwr = convert(rel))`, where `convert` turns the array into an integer representation. This then returns two suggestions for the next word to guess according to the two different algorithms, along with some statistics and a copy of all the remaining possible words. It is possible to pass this list of remaiining words in the `answers` argument to save on computation.

Switching word lists isn't as simple as it should be currently, there's a few places in the code that have to be changed manually to support it, I'll try fixing this in a future update.

## Lookup Table
Currently the code relies on a 200MB lookup table for quickly calculating the relation between two words. This isn't included in the repository so is generated in memory, and can then be saved manually if desired.
