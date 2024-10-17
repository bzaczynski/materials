In this lesson, I'm going to walk you through one possible solution for replicating how the Unix wordcount command handles data supplied through standard input, which most often comes from your keyboard.

I'm currently in my GitHub Codespaces environment with the project already set up. When I open the terminal and run the `pytest` command, it'll show us the overall progress:

```sh
$ pytest
```

This output includes the statuses of the acceptance criteria for the current task, as well as any previous tasks. Unsurprisingly, many of these criteria are yet to be addressed, which is why they're shown in red here.
 
To pull up more detailed instructions, we can open the corresponding page on Real Python by typing `pytest --task`:

```sh
$ pytest --task
```

The first time around, you'll need to tell VS Code that it's safe to trust the `realpython.com` domain. Once you do, it'll open a page with instructions. You can arrange your workspace so that you have these instructions conveniently accessible to the side:

> Win + Left, Win + Right

Here on the left, you can see the list of acceptance criteria, followed by a few practical examples. You don't need to strictly follow them in order. Start with the criterion that feels most approachable to you. Why don't we begin at the bottom, where it states that the program should output zero lines, zero words, and zero bytes if provided with an empty input stream:

> Highlight the last acceptance criterion.

To address this, we can hard-code the expected output from the first example:

> Highlight "0 0 0"

We'll do that by printing the string literal as "zero-zero-zero":

```python
def main():
    print("0 0 0")
```

Let's save the file and re-run pytest to check for any changes:

```sh
$ pytest
```

And there we go! The first acceptance criterion is now green, which means that we're already making some progress. As we tackle more constraints, they'll nudge us to further refine the code.

Another useful step is to manually test your command. Let's try running `wordcount` from the terminal using the provided example:

(Copy and paste?)

```sh
$ echo -n | wordcount
0 0 0
```

That looks promising. However, if we change the input by letting the `echo` command append its usual newline character at the end of the stream, then the output won't yet reflect this:

```sh
$ echo | wordcount
0 0 0
```

The expected outcome should account for the invisible newline character that we've just introduced. More specifically, the output should indicate one line, zero words, and one byte, or one-oh-one. This mismatch happens because we haven't yet read from standard input.

In Python, there are a couple of ways you can read data from standard input. But, one of the most straightforward ones involves the `sys` module, so let's import it now: 

```python
import sys

# ...
```

The `sys` module exposes standard input through the `stdin` attribute, which, in turn, comes with the `.read()` method. If we don't provide any arguments to the method, then it'll read everything until an End-of-File character or when data runs out:

```python
import sys

def main():
    sys.stdin.read()
```

This method returns a Python string object, which we can store in a new variable called `text`, as it contains a sequence of characters:

```python
import sys

def main():
    text = sys.stdin.read()
```

Next, we'll count the lines, words, and bytes in this text.

To find the number of lines, we can call the string object's `.count()` method with a special sequence as an argument. The backslash-n is a special character that represents an invisible line break in the string:

```python
import sys

def main():
    text = sys.stdin.read()
    text.count("\n")
```

Let's assign the result to another variable. It's always a good idea to give your variables descriptive names, so we'll go with `num_lines`, for number of lines, in this case:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
```

This handles the line count well, even accounting for different newline styles across operating systems.

But, counting words is more tricky. According to the definition provided in the task's description, a word is any sequence of characters delimited by whitespace, like spaces or tabs. That's not exactly how the original wordcount command defines words, but it'll do. 

To extract words, we can leverage the string object's `.split()` method, which divides a string into substrings based on the given separator. By default, if we don't provide any separator, then this method splits on whitespace, which is precisely what we need:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    text.split()
```

With a list of words in place, we can check its size by calling the built-in `len()` function on it:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    len(text.split())
```

Similarly, we'll assign the result to a properly named variable, like `num_words`:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
```

The last missing piece is the number of bytes in the text. To keep things simple, we'll equate the byte count with the string length for now:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(text)
```

Finally, we can print these variables, separating them with spaces:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
    num_bytes = len(text)
    print(num_lines, num_words, num_bytes)
```

Let's re-run pytest to verify our solution:

```sh
$ pytest
```

Awesome! We've made it to the next task, which involves handling non-English characters. You can click the link that appears in the terminal to view the specific details on Real Python.
