To use:

```
pip3 install jsonpath-ng
./test-xmltodict.py 
```

You can specify any other file:
```
./test-xmltodict.py -f mds.edugain.org
```

You can specify things to search for:
```

./test-xmltodict.py -s https://refeds.org/sirtfi
./test-xmltodict.py -s http://refeds.org/category/research-and-scholarship
./test-xmltodict.py -s http://www.geant.net/uri/dataprotection-code-of-conduct/v1
```

### The catch:

I'm using this to find stuff:
```python
result = parse('$.*.*[*].*.*[*].*[?*[*]="'+args.search+'"]').find(jsondata)
```

The more specific alternative was:
```python
result = parse('$.*.md:EntityDescriptor[*].md:Extensions.mdattr:EntityAttributes[*].saml:Attribute[?saml:AttributeValue[*]="'+args.search+'"]').find(jsondata)
```

But the search string cannot contain colons and other special characters.

This also does not work terribly well for things one needs to find on
different levels, such as the registrationAuthority

It's a bit messy, but demonstrates what we discussed ealier
.
