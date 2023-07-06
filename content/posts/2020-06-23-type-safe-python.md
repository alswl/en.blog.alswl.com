---
title: "Type system in Python"
author: "alswl"
slug: "type-safe-python"
date: "2020-06-23T17:54:00+08:00"
tags: ["python"]
categories: ["coding"]
---

![wall](../../static/images/upload_dropbox/202006/wall.png)
<small>image from pixabay.com</small>


Static typing is becoming more and more popular.
Several languages born after 2010, Go, Rust, TypeScript, etc., have gone the static typing route.
Some of the previously popular dynamic languages (Python, PHP, JavaScript) are also actively introducing new language features (Type Hint, TypeScript) to enhance static typing.

Having worked on larger projects in Python, I have experienced the difficulties that dynamic languages pose when projects get large:
The cost of code regression during the refactoring phase was unusually high, and much of the historical code was afraid to move.
Then the technology stack shifted to Java, and being embraced by the type system made people feel safe.

In the last year, I have been working on a stability-oriented operation and maintenance system. Python was used at the beginning of the system selection.
I pushed Python 3.7 in the project and used Python's type system on a large scale to mitigate potential risks.

Going back to my roots, I spent some time learning about Python's design and implementation of the type system.
This article is a PEP proposal that describes how far Python has come with the type system.

<!-- more -->


## Type Systems

Before we talk about type systems, we need to clarify two concepts, dynamic languages and dynamic types.

A dynamic programming language is a program that can change its structure at runtime.
This structure can include functions, objects, variable types, and program structures.
Dynamic types are one type of Type System, i.e., programs that can modify variable types during runtime.
The other type is the static type: the variable type is determined at compile time and is not allowed to change at runtime.
Another division of the type system is strong and weak types, where strong types are instructions that forbid type mismatches and weak types vice versa.

The two concepts, dynamic languages and dynamic types, have different entry points.
Python is a dynamic language and a dynamically typed language, or a strongly typed dynamic type.
This article will focus on the type system of the Python language and will not cover dynamic language features.


## The road to type safety

There is an ongoing debate within the industry about which is more powerful: dynamic or static types.
Proponents of static types see advantages in three areas: performance, error discovery, and efficient refactoring.
Static types can significantly improve runtime efficiency by determining the concrete type at compile time;
The ability to detect errors at compile time, especially when projects get progressively larger;
The type system can help the IDE to prompt for efficient refactoring.
Proponents of dynamic typing argue that analyzing code is simpler, less error-prone, and faster to write.

Python developers have not failed to see this pain point.
A series of PEP proposals were created.
The type system was introduced to Python through syntax and feature enhancements while retaining the benefits of Python's dynamic type system.

Python proposed PEP 484 in 2014, followed by a refined version of PEP 483 (The Theory of Type Hints).
Its project implementation, the [typing](https://docs.python.org/3/library/typing.html) module, was released in 3.5.
After several iterations of PEP 484, PEP 526, PEP 544, PEP 586, PEP 589, and PEP 591, Python's type system has become very rich.
It even includes relatively rare features like Structural Subtyping and Literal Typing.

### PEP 483 - Core Concepts

Released in December 2014, [PEP 483](https://www.python.org/dev/peps/pep-0483/)
This is a concise version of the core concepts Guido wrote, making clear the direction, boundaries, do's and don'ts of building a type system for Python.


PEP 483 does not talk about concrete engineering implementations, but rather outlines how the Python type system is presented to the public.
Define the Type/Class difference, the former being a syntactic analysis concept and the latter a runtime concept.
Under this definition, a Class is a Type, but a Type is not necessarily a Class.
For example, `Union[str, int]` is a Type but not a Class.

PEP 483 also introduces built-in base types: `Any` / `Unison` / `Optional` / `Tuple` / `Callable`, which support rich upstream variations.

The biggest criticism of the static type system is that it is not flexible enough, and the Go language does not implement generics yet.
PEP 483 introduces the use of Python Generic types in a generic
The form is as follows:

```python
S = TypeVar('S', str, bytes)

def longest(first: S, second: S) -> S:
    return first if len(first) >= len(second) else second
```

Finally, PEP 483 also mentions some important minor features:

- Alias Alias
- Farward Reference (use definition class in definition class method annotations), eg.: solves the problem of needing to reference a Node in a binary tree Node node
- covariance contravariant
- Use annotations to mark types
- Transformation Cast


The implementation of PEP 483 relies heavily on [PEP 3107 -- Function Annotations](https://www.python.org/dev/peps/pep-3107/).
This proposal. PEP 3107 introduces the use of function annotations. For example, `func(a: a1, b: b1) -> r1`This code, thewhere the descriptors after the colon are recorded in the `__annotations__` variable of func.

PEP 3107 shows the effect as follows, where you can clearly see that the function variables are stored:


```python
def add(x: int, y: int) -> int:
    return x + y

add.__annotations__
# {'x': int, 'y': int, 'return': int}
```

PS: Python now has Decorator decorators / Annotation annotations, where Annotation is also designed with the same name as Java's Annotation, a potpourri.


### PEP 484 - Type Hints Core

[PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/) 
A complete description of how the Python type system is designed, how it is used, and what the details are (typing modules), building on PEP 483

This proposal begins by stating:

> Python will remain a dynamically typed language, and the authors have no desire to ever make type hints mandatory,
> even by convention.

In one sentence, the proposal eliminates the possibility of Python evolving to a static system at the language level.

In addition to the features already explained in PEP 483, the proposal also appeals to me in the following ways:

- Allow adding type descriptions to already existing libraries via Stub Files. Specifically, the typed signature of Python code is described using the `.pyi` file corresponding to the Python file.
  This scheme is similar to TS's `@types` file.
- Allowing type overloading with `@overload` is a long time coming, and Python can actually (in a sense) support overloading.
- Introduces typing implementation details, such as using abs (Abstract Base Class) to build interfaces for common types, including `Sized` / `Iterable` base interfaces.
  Personally, I think this is actually quite a lot of work, and is a way to sort out the dependencies of existing classes.
- Python backward (Python 2) compatible methods are introduced, and there are several strategies:
  Using decorator (`@typehints(foo=str, returns=str)`), comments, Stub files, Docstring


### PEP 526 - Variables are also arranged

[PEP 526 - Syntax for Variable Annotations](https://www.python.org/dev/peps/pep-0526/)
The core proposal is to add Type Hints support to variables.

Similar to `function annotation`, it is also stored by annotation.
The difference is that instead of adding a `__annotations__` member to the instance, the annotations information for the variable is stored in the context variable `__annotations__`.
This is actually quite understandable: when a variable type is defined, the variable is not yet initialized.

I'll write a demo to demonstrate this:


```python
from typing import List
users: List[int]

# print(__annotations__)
# {'users': typing.List[int]}
```

As you can see, the above demo has the effect of creating a `users` in the context variable, but this `users` doesn't actually exist, it just defines the type.
If you run `print(users)` it will throw `NameError: name 'users' is not defined`.

It is clearer to look at the bytecode:

```
 L.   1         0  SETUP_ANNOTATIONS

 L.   1         2  LOAD_CONST               0
                4  LOAD_CONST               ('List',)
                6  IMPORT_NAME              typing
                8  IMPORT_FROM              List
               10  STORE_NAME               List
               12  POP_TOP

 L.   3        14  LOAD_NAME                List
               16  LOAD_NAME                int
               18  BINARY_SUBSCR
               20  LOAD_NAME                __annotations__
               22  LOAD_STR                 'users'
               24  STORE_SUBSCR
               26  LOAD_CONST               None
               28  RETURN_VALUE
```

As you can clearly see, instead of creating a variable named users, the `__annotations__` variable is used.
Note: Python stores variables using the opcode `STORE_NAME`.

PS: There are a number of rejected proposals in this proposal, which is quite interesting, and the community has come up with a lot of strange and clever ideas.
You can see the caution of the community decision, the difficulty of upgrading the stock system.


### PEP 544 - Nominal Subtyping vs Structural Subtyping

The type system discussed in PEP 484 is Nominal Subtyping.
This [PEP 544 -- Protocols: Structural subtyping (static duck typing)](https://www.python.org/dev/peps/pep-0544/)
This [PEP 544 -- Protocols: Structural subtyping (static duck typing)]() is proposed for Structural subtyping.If I had to translate it, I think it could be called named subtypes / isomorphic subtypes.
Note that some people also refer to Structural Subtyping as Duck Typing, but the two are not the same, see
[Duck typing / Comparison with other type systems](https://en.wikipedia.org/wiki/Duck_typing#Structural_type_systems).

Nominal Subtyping refers to matching types literally, while Structural Subtyping matches by structure (behavior).
For example, Go's Type is a Structural Subtyping implementation.

Here is a simple demo to demonstrate the latter:

```python
from typing import Iterator, Iterable

class Bucket:
    ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[int]: ...

def collect(items: Iterable[int]) -> int: ...
result: int = collect(Bucket())  # Passes type check

```

The code defines the type Bucket and provides two class members. These two class members happen to be the definition of Interator.Then in practice, you can use Bucket instead of Iterable.

### PEP 586 / PEP 589 / PEP 591 Continuous enhancement

[PEP 586 -- Literal Types](https://www.python.org/dev/peps/pep-0586/)
The Python 3.8 implementation supports the use of literals as types.
For example `Literal[4]`, and for a more semantic example `Literal['GREEN']`.

My first thought was that this is very similar to Symbol in Scala, which is written as `Symbol("GREEN")`.
This feature is quite collegial and easy to write in the DSL.Scala officials have said that the Symbol feature may be removed in the future, so it is recommended to use constants instead.

[PEP 589 -- TypedDict: Type Hints for Dictionaries with a Fixed Set of Keys](https://www.python.org/dev/peps/pep-0589/)
Add a Type of key to Dict, inheriting from `TypedDict`.

[PEP 591 -- Adding a final qualifier to typing](https://www.python.org/dev/peps/pep-0591/)
Add the concepts of `final` / `Final`, the former is a decorator, the latter is an annotation that marks the class/function/variable as unmodifiable.

At this point, Python 3.8 has the type system features we need every day (not at runtime 😂).

## Summary

Unfortunately, the `typing` module is clearly marked in the documentation as:

>  The Python runtime does not enforce function and variable type annotations. They can be used by third party tools
>  such as type checkers, IDEs, linters, etc.

Namely, the Python runtime (Intercepter / Code Evaluator) does not support type decorators for functions and variables.
These decorators can only be checked by third-party tools, such as type checkers, IDEs, statics, and Linter.

This information illustrates the limitations of Python's attempts at type safety. All the restrictions, constraints, and limitations don't happen at runtime.
The only way to harvest engineering-above-board value from the type system is to use third-party tools.

It's true that the Python community is trying to move closer to a type system, but how far can this non-language level Runtime support go?
Python lacks a golden father, and its godfather Red Hat has limited resources to invest. Even the community hasn't finished switching from Python 2 to Python 3 yet, so why?
The input/output ratio is too low, the new features are not attractive enough, and there are too many alternatives.

On the other hand, look at the competition:
Dynamic languages are moving closer to static languages, and static languages are absorbing features from dynamic languages. For example, the REPL (Read-Eval-Print-Loop) in Java 14.
Kotlin / Scala and other languages Type Inference.
Perhaps this evolution is more acceptable to users.


## 参考

- [typing — Support for type hints — Python 3.8.3 documentation](https://docs.python.org/3/library/typing.html)
- [PEP 483 -- The Theory of Type Hints | Python.org](https://www.python.org/dev/peps/pep-0483/#type-variables)
- [PEP 484 -- Type Hints | Python.org](https://www.python.org/dev/peps/pep-0484/#abstract)
- [the state of type hints in Python](https://www.bernat.tech/the-state-of-type-hints-in-python/)
