In this lesson, I'm going to show you one possible way to solve this task by satisfying its acceptance criteria.

I'm in my GitHub Codespaces environment where I have the project already set up. When I go the terminal and type the `pytest` command without any arguments, it'll show me the statuses of the acceptance criteria for the current task as well as the past ones:

```sh
$ pytest
```

Of course, most of these criteria are yet to be addressed, which is why they're shown in red here.

I can also pull up the corresponding page on Real Python by typing `pytest --task`:

```sh
$ pytest --task
```

The first time you do this, you'll have to tell VS Code that it's safe to trust the realpython.com domain. When you do, it'll open the page with instructions, which I'll move to the side so that I have them at my fingertips:

Win + Left, Win + Right

And, here, on the left are the acceptance criteria followed by a few examples. Note that you don't have to strictly follow them in order. Just pick one that's the most straightforward to you at the moment. For instance, why don't we start from the bottom. It says that the program should report zero lines, words, and bytes in case of an empty input stream:

> Highlight the last acceptance criterion.

For now, I can hard-code the expected output from the first example:

> Highlight "0 0 0"

...by printing the string literal "zero-zero-zero":

```python
def main():
    print("0 0 0")
```

Now, I can save the file and re-run pytest to see if there's any change:

```sh
$ pytest
```

There is! The first acceptance criterion is lit in green now, which means that we're already making some progress. Of course, as we add more constraints to the problem, it'll force us to update the code in a way that we're still heading in the right direction.

Another thing I can do is run the `wordcount` command manually from the terminal, for instance, using one the provided examples:

```sh
$ echo -n | wordcount
0 0 0
```

That's great. However, as soon as I change the input, by letting the `echo` command append the trailing newline, as in the second example, we won't see any difference in the command's output:

```sh
$ echo | wordcount
0 0 0
```

Well, the expected value is different. Since there's an invisible line break character in the input, the command should have reported one line, zero words, and one byte, or one-oh-one. This discrpancy is because we don't actually read anything from standard input.

There are a couple of ways to read data from standard input in Python. But, one of the most straightforward ones involves the `sys` module, so I'm going to import it now:

```python
import sys

# ...
```

This module conveniently exposes the `stdin` object, which stands for standard input. I can call the `.read()` method on it. If I don't provide any arguments to the method, then it'll keep reading data until encountering the End-of-File control character or when there's no more data in the stream:

```python
import sys

def main():
    sys.stdin.read()
```

This method returns a Python string object, which I can assign to a new variable that I'm going to call `text`, since it contains a string of characters:

```python
import sys

def main():
    text = sys.stdin.read()
```

And now, I can count the number of lines, words, and bytes in the text.

To find the number of lines, I can call the string object's `.count()` method with a special sequence as an argument. The backslash-n is special character that represents the newline character or the line break that appears in the string:

```python
import sys

def main():
    text = sys.stdin.read()
    text.count("\n")
```

Let's assign the result to another variable. It's always a good idea to give your variables descriptive names, so I'll go with `num_lines` in this case:

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
```

Okay. We can determine the number of lines in the text by counting the number of so-called line feed characters. This already takes into account the differences across newlines on various operating systems. 

But, finding the number of words is a bit more tricky.

According to the definition provided in the task's description, a word is any sequence of characters delimited by whitespace, such as a space or a tab. That's not exactly how the original wordcount command defines words, but it'll do. 

So, to find the number of words in the text, we can check the length of a list of substrings that represent those words: 

```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len()
```




```python
import sys

def main():
    text = sys.stdin.read()
    num_lines = text.count("\n")
    num_words = len(text.split())
```