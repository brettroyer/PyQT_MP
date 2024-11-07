# parallel-processing-pyqt: Parallel Processing From PyQt5

## Introduction
I created this concept application to _hopefully_ help others and to garner constructive feedback as to how it might be improved.

**Please Note:** I have used a more complex version of this code in an application that streams and analyzes intraday stock market data from the Schwab Developer API, so I can vouch that the general principles work in *real life*. (However, please thoroughly **TEST** whatever you end up doing with it!)

## The Problem
- PyQt applications have a main thread of execution: **the GUI thread**.
- Typically, anything called directly from PyQt (object method calls, scripts, etc.) is run on the GUI thread.
- This results in everything running **synchronously**, one task at a time - which can be impractical for sophisticated applications, as long running tasks will cause the GUI to **freeze** (Not good!)
- PyQt does offer **multithreading**, which allows for subprograms to be run, in thread(s), separate to the GUI thread, to prevent the freezing problem.
  - This can often be all that is required, and if that is all you need, this application can still help you with that!
  - Simply adjust the _thread_worker_ module so it no longer instantiates _ParallelSupervisor_.
- However, if **multiprocessing** is required, things get even more complicated.
  - multithreading and multiprocessing need to be combined.

## This Solution
- This solution demonstrates combining multithreading (with PyQt [QThread](https://doc.qt.io/qt-6/qthread.html)) with multiprocessing, via [RAY](https://www.ray.io/).
  - I chose RAY because I find it easier to work with, and the principles of how to communicate between multiprocessing and PyQt are similar, regardless of the library you use.
- **Please note**: This is definitely **not** a demonstration of how to do multiprocessing - that's a big topic, out of the scope of this.
- This solution also employs an *adaptation* of the [Model-View-ViewModel](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel) design pattern, because:
  1. I think it's good practice, and I'm trying to use it more.
  2. It actually lent itself, very nicely, to this particular problem.
- Before you begin, I **strongly** suggest you take a look at the links in the [Reference Sources](#reference-sources) section.
  - These are where I got my inspiration from, and it makes it much easier to understand some of the design decisions.

## Things to Consider
- The multiprocessing that takes place in *this* application is nothing very useful, and wouldn't be worth the overhead. It simply generates numbers from 0..*.
- If you are interested in adapting this to multiprocess with something a little more interesting, you could take a look at: [ray-streamer](https://github.com/IanAtDazed/ray-streamer) where we simulate streaming stock prices and processing them in parallel before returning them to something like this.
- If you are doing anything critical with this, **please** fully test it first!

## Feedback
- If you have any constructive feedback as to how the process, code, or documentation might be improved, I would love to hear from you.

## Reference Sources
I **strongly** recommend you read, at least, the first two of these articles, and if you don't have knowledge of MVVM, at least the 3rd.

- [Doing python multiprocessing The Right Way](https://medium.com/@sampsa.riikonen/doing-python-multiprocessing-the-right-way-a54c1880e300)
- [Use PyQt's QThread to Prevent Freezing GUIs](https://realpython.com/python-pyqt-qthread/)
- [A Clean Architecture for a PyQT GUI Using the MVVM Pattern](https://medium.com/@mark_huber/a-clean-architecture-for-a-pyqt-gui-using-the-mvvm-pattern-b8e5d9ae833d)
- [Model–view–viewmodel](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)
- [Model-View-ViewModel (MVVM)](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm)
