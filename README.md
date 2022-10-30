# librenms_apidoc
Create documentation by pulling information from a LibreNMS monitoring system instance, using librenms-handler and API interaction: https://github.com/WhaleJ84/librenms_handler

<h1>Project Status: testing</h1>

- Not 10/10 on pylint right now...
- <b>verify = False ... is SSL verify False... you can set to True if you want...</b>

<h2>Requirements</h2>

- requires python3
- requires pip3 install of modules in requirements.txt - recommend run as unpriv user

<h2>Introduction</h2>

Use this script to output a file using python module `tabulate` e.g. RST/CSV. 

The file is created by the script which queiries your LibreNMS monitoring system instance. It works through LibreNMS `device groups`, obtaining info for each host in the `device group`. Therefore its good to have these groupings in order either via GUI or API.

Global variables including the access token are defined in `librenms_apidoc_settings.py`, by default the output is a pandas dataframe in RST format. You could change that to something else (.e.g CSV).

<h2>Additional details</h2>

- You need your LibreNMS URL configured and TOKEN in `librenms_apidoc_settings.py`
- A regex in the code stops VMWare serials/macs manifesting in the output, simple replacing with the word VMWare.
- You can configure groups to exlude in `librenms_apidoc_settings.py`


<h2>Setup</h2>

Install pip3 requirements for this project.

`pip3 install --user -r requirements.txt`

Configure `librenms_apidoc_settings.py` as mentioned. TOKEN + URL at very least.

Run the script, output is in `CWD`.

`./librenms_apidoc.py`

<h2>Further setup - Envisaged usage</h2>

Use a cronjob and/or gitlab CI. Upload content automatically to Wiki or internal web server you have control of.
