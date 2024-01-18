# Movies web scraping

## Technical Details

The algorithm is written in Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux.
The first stable released version is V1.

## Objective
The script downloads the movies data from the famous website 'Rotten Tomatoes'. The objective is to find the best movies we can find on the 3 best streaming platform at the moment:
- Netflix
- Disney Plus
- Amazone Prime Video

The (positive) side effect of this algorithm is to finally find an answer to the question: "Which film do I whatch tonight?" (or at least simplify the choice).

## Data
The script download the movies data from the famous website 'Rotten Tomatoes'.
The movies are sorted from the best to the worst, based on critic and audience score.

## Data output
The output is a txt file that contains 3 different tables (written in markdown style):
1. The best 20 recent[^1] films released on the 3 streaming platforms
2. The best 3 film for each platform, sorted by audience and critic score
3. The best 3 film for each platform, sorted by the global score ( mean between critic and audience score)


[^1]: last review maximum 30 days before the day of the script's launch
