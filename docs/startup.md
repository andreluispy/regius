[Return to README](../README.md)

# Making the Env
 1. Download the GNU Regius compiler
    - Download the compiler: [Not Avaible]()
 2. Download C Compiler
    - Download the GCC to linux/mac or MingW to Windows
        - Linux: `sudo apt-get install gcc`
        - MAC: `brew install gcc`
        - Windows: [http://mingw-w64.org/doku.php/download](http://mingw-w64.org/doku.php/download)
 3. Write Code!

# Writing Hello World
 Create the script: `script.rgs`. Write:

```c
import stdio;

print("Hello World\n");
```

 Use `import` to import one lib, the `stdio` is the Standart Lib for Input and Output. The `print` command is a function of `stdio` to print string in terminal.

# Vars
 Use the comand `var` to create a var:
 ```c
var myvar = "Hello";
 ```

# PRINTF
 Use **printf** to print formated strings

 ```c
import stdio;

var name = "Andre";
printf("%s\n", name);
 ```

 Use `%s` to strings vars, use `%i` to int vars

# raw_input
 Use **raw_input** to get user inputs in string format:

```c
import stdio

raw_input(name); // Args: var to get input
```