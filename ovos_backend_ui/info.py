APP_INFO = """<div id="info"><p>
This is an app to control a <a href='https://github.com/OpenVoiceOS/ovos-personal-backend' target='_blank' rel='noopener noreferrer'>local backend</a></p>

<p>Admin users have full control over the backend.
Any user creation and removal, device creation and removal,
and any other things that the backend allows.</p>

<p>Users are limited to specific devices specified by
permisions set by the Admin user.</p>

<p>Not all features are implemented yet.
Check back often for updates</p>

<p>This is an alpha version, please leave feedback <a href='https://github.com/builderjer/ovos-backend-ui/issues' target='_blank' rel='noopener noreferrer'>here.</a></p>

<p>Author: BuilderJer</p></div>"""

TOOLTIPS = {
    "DEVICE_AUTHENTICATION": """Device Authentication

Disable device authentication.

Disable ONLY if you know what
you are doing.
(ovos-qubes) for example""",

    "OVERRIDE_LOCATION": """Override Location

When set to 'True', the
location set in the backend
will be used.

Either this or 'GEOLOCATE'
can be used, NOT both""",

    "GEOLOCATE": """IP Geolocate

When set to 'True', the
location will be set by
the IP aqquired.

Either this or OVERRIDE LOCATION
can be used, NOT both""",

    "SELENE_PROXY": """Selene Proxy

When set to 'True',
the Mycroft Selene can be used.

Usefull for using a single pairing to
Mycroft Selene backend for all of
your connected devices""",

    "TTS": """Default TTS

This sets the default voice
that is heard on your device""",

    "WAKEWORD": """Default Wakeword

Custom wakewords?
ABSOLUTLY!!""",

    "DATE_FORMAT": """Date Format

Either set to DMY (Friday, 25 November 2022)
or MDY (Friday, November 25 2022)""",

    "TIME_FORMAT": """Time Format

This the clock on your device to use
'full' - 24hr format
'short' - 12hr format""",

    "SYSTEM_UNITS": """System Units

Sets your system to use
'metric' - celsius, kph, etc... or
'imperial' - faherinheit, mph etc..."""
    }

NO_ADMIN = """<p>There is no Admin user available.</p>

<p>The usage of this app will be limited.</p>

<p>Talk to your backend administrator to
setup an administrator</p>

<a href="auth/login"><button type="button" class="btn_lt_bkgnd text-center">
    Continue
    </button></a>"""

NO_USERS = """<p>There are no users configured.</p>

<p>An admin user must be created to use this app</p>

<p>Run <code>setup_admin.py</code> from the install
directory and refresh the page.</p>

<a href="/"><button type="button" class="btn_lt_bkgnd text-center">
    Continue
    </button></a>"""

NO_USER = """<p>There is no user registered by that name.</p>

<p>Check your login info and try again</p>

<a href="login"><button type="button" class="btn_lt_bkgnd text-center">
    Continue
    </button></a>"""

WRONG_PASSWORD = """<p>Username and Password do not match</p>

<p>Check your login info and try again</p>

<a href="login"><button type="button" class="btn_lt_bkgnd text-center">
    Continue
    </button></a>"""
