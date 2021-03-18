# Archival Spider [![Donate to the founder](https://img.shields.io/badge/Donate-Ko‒fi-green.svg)](https://ko-fi.com/surbubianjesus) 

#### Efficient means to documenting your projects info.</h4>
[![Educational/Experimental project](https://img.shields.io/badge/python-experimental-orange.svg?style=flat)](https://github.com/netrules/archival-web-spider)
[![Contribute to the repo](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/netrules/archival-web-spider/issues)
[![Compliant with TravisCI standard](https://travis-ci.com/netrules/archival-web-spider.svg?branch=master)](https://travis-ci.com/netrules/archival-web-spider)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/netrules/archival-web-spider) 
[![Accepting contributions](https://codeclimate.com/github/netrules/archival-web-spider/badges/gpa.svg)](https://codeclimate.com/github/netrules/archival-web-spider) 
[![Known Vulnerabilities](https://snyk.io/test/github/netrules/archival-web-spider/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/netrules/archival-web-spider?targetFile=requirements.txt)
[![Code coverage](https://codecov.io/gh/netrules/archival-web-spider/branch/master/graph/badge.svg)](https://codecov.io/gh/netrules/archival-web-spider) 
[![HitCount](https://hits.dwyl.com/netrules/archival-web-spider.svg)](https://hits.dwyl.com/netrules/archival-web-spider) 

## Inspired By
Project inspired by the likes of archive.org and miscellaneous free archival and curation projects. Intended to work for a broader public with a larger objective.

## About
Python project which uses mainly BeautifulSoup and Selenium Webdriver in order to crawl through websites and retrieve their resources in order to keep a personal record of documentation studied. Not meant to be used without webmasters permissions; this is only for learning purposes. [We do not encourage you to breach terms of any website.](https://towardsdatascience.com/web-scraping-with-python-a-to-copy-z-277a445d64c7)

## To-do
- Included files within script should be able to:
	- Follow principles of deduplication based filesystem such as: [Duplicacy - Cloud Backup Tool](https://duplicacy.com/), [Borg - Deduplicating Archiver](https://github.com/borgbackup/borg), [SDFS - Deduplicating FS](https://github.com/opendedup/sdfs)
	- Permit elastic mapping as external scripts continue to be stored in CDN for using network bandwidth instead
	- Inline styles by using [Pynliner - CSS-to-inline-styles conversion tool](https://github.com/rennat/pynliner)
- Can follow principles of mind mapping and memory techniques, such as:
	- [Learn Anything](https://learn-anything.xyz/#!)
	- [Anki Flash Cards](https://apps.ankiweb.net/)
- Make decentralization possible due to browsing websites offline, saved per domain
- Add as pip package
- Zipper to minimize manual operations by automatizing and streamline
- Add silent mode

## Troubleshooting

### Common Issues:

#### Chrome not running!
With issues like `selenium.common.exceptions.WebDriverException: Message: unknown error: session deleted because of page crash`, do the following:
> Try `ps aux` and see if there are multiple processes running.
> In linux, with `killall -9 chromedriver` and `killall -9 chrome` you can make sure to free up processes to run the app again.
> In windows, the command is: `taskkill /F /IM chrome.exe`.
> This is usually a result of crashes mid-runs, and is easily fixable.

####   ..."encodings\cp1252.py", line 19, in encode...
UnicodeEncodeError: 'charmap' codec can't encode characters in position XXXX-YYYY: character maps to <undefined>
> This is a windows encoding issue and it may be possible to fix by running the following commands before running the script:
> `set PYTHONIOENCODING=utf-8`
> `set PYTHONLEGACYWINDOWSSTDIO=utf-8`

## Donate
Donate if you can spare a few bucks for pizza, coffee or just general sustenance. I appreciate it.

[![Donate Button](https://img.shields.io/badge/Donate-Ko‒fi-green.svg)](https://ko-fi.com/surbubianjesus)
