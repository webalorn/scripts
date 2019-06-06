# Some scripts I made

## Coding scripts

These are script usefull for coding. There is currently only `cpp_executor`, with `g++11.cpp`, `g++14.cpp` and `g++17.cpp` using different versions of C++ with  this script. You can compile it just by using (here, for `g++11`):

```bash
g++ -std=c++11 -o g++11 g++11.cpp
```

## auto_scripts

These script are aimed to automate some tasks:

-   `leekwars.py`: automaticly do all fights on the [leekwars game](https://leekwars.com).
-   `manawyrd.py`: daily connection on [manawyrd](https://www.manawyrd.fr/index.php) and get daily reward.
-   `start.sh`: run all scripts.

The passwords must be stored in the directory `passwords`, at the root of the project, in a file with a name corresponding to the script: `passwords/leekwars` for `leewars.py`, and `passwords/manawyrd` for `manawyrd.py`. Format of a file:

```
username
password
```

One can add in the starting programms:

```bash
gnome-terminal -e "bash -c \"chemin/vers/le/script/start.sh ; exec bash\""
```