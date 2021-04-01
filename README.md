# Firewall Block Lists

This is a new repo which still has some rough edges.  Please feel free to add pull requests for improvements.

The main scriptt is Python based and you will need to install a couple of packages to get in running:

```bash
pip install netaddr pyyaml
```

The `lists.yml` file contains input block lists, you can add more here.  Should be clear how to do this, but let me know if anything is unclear. The format field will be cidr for most lists you want to add.  The INternet Storm Center DShield list has a different format to these (take a look at the downloaded file).  If you need to add lists with a similar format, which give an IP Range between two IP addresses, instead of an standard CIDR range, use `range` as the format.

The main script processes the lists and compresses any CIDR ranges which can be compressed and prints some stats on the list.  It prints out a comparison, showing the number of entries found in any combination of two lists.


# Features to add

- Output of a single unified IP list for use in firewalls, like pf

- Cleaner output of comparison, into a csv file
