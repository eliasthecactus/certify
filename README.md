
<h1 align="left">certify</h1>
<p>
  <a href="https://github.com/eliasthecactus/certify#readme" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/eliasthecactus/certify/graphs/commit-activity" target="_blank">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  </a>
  <img alt="Version: v1.0.0-alpha1" src="https://img.shields.io/badge/version-v1.0.0--alpha1-blue" />
  <a href="https://github.com/eliasthecactus/certify/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/github/license/eliasthecactus/certify" />
  </a>
</p>

> 😋 A lightweight python CLI/WebGUI SSL-certificate checker with alert function

## Install
```sh
git clone https://github.com/eliasthecactus/certify.git
cd certify/
pip install -r requirements.txt
```

## Usage
```sh
Usage: python certify.py [OPTION] ...

-d, --delete        Delete a domain from the db
    --all           Clear the table or delete the db
-a, --add           Add a domain to the db
-l, --list          List domains in db
    --all           To print more details
-u, --update        Update expiry date
-c, --create        Create file
    --pdf

Example:
python certify.py -c pdf
python certify.py --delete google.com 443
python certify.py --list
```


## 📃 ToDo
- [x] full list and simple list
- [ ] Server mode
- [ ] PDF generator
- [ ] get data as json
- [ ] get specific value


## Author
👤 **elias**
* Instagram: [@eliasthecactus](https://instagram.com/eliasthecactus)
* Github: [@eliasthecactus](https://github.com/eliasthecactus)


## 🤝 Contributing
Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/eliasthecactus/certify/issues).


## Show your support
Give a ⭐️ if this project helped you!


## 📝 License
[Copyright](https://github.com/eliasthecactus/certify/blob/main/LICENSE) © 2022 [eliasthecactus](https://github.com/eliasthecactus)
