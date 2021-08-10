[Return to README](../README.md)

# Making the Env
 1. Download the compiler
    - Download the compiler: [Not Avaible]()
 2. Download C Compiler
    - Download the GCC to linux/mac or MingW to Windows
        - Linux: `sudo apt-get install gcc`
        - MAC: 
          - If you have the most recent Apple Command Line Tools (macOS 10.nn) for Xcode installed for your operating system version — get from [developer.apple.com/download/more](developer.apple.com/download/more), then you need a package manager(e.g.  homebrew) to install, and compile GCC and all of its dependencies. That compilation process will take at least an hour. After you initially install homebrew (brew):

            ```
            export HOMEBREW_NO_ANALYTICS=1

            brew update

            brew upgrade

            brew info gcc

            brew install gcc

            brew cleanup
            ```

            The gcc application will be installed by default in /usr/local/bin.
        - Windows: [http://mingw-w64.org/doku.php/download](http://mingw-w64.org/doku.php/download)
 3. 
