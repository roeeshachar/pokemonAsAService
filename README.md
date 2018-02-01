**Requirements**

```
sudo apt-get install python-virtualenv
virtualenv venv
source venv/bin/activate
```
```bash
./installRequirements.sh
```
Create settings file _settings.conf_ as follows:
 ```
[ElasticSearch]
host = "localhost"
port = 9200
index = "paas"
doc_type = "pokemon"
```

To run the server run app file _paasAPI.py_