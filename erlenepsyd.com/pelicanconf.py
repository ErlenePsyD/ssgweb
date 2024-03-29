AUTHOR = "Erlene Rosowsky"
SITENAME = "the older self"
# pelican-seo requires a site URL
SITEURL = "https://erlenepsyd.com"
PATH = "content"
STATIC_PATHS = ["images", "images/favicon.ico"]
EXTRA_PATH_METADATA = {"images/favicon.ico": {"path": "favicon.ico"}}
# Set to False before deploying to production
RELATIVE_URLS = True
FAVICON = "images/favicon.ico"
TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("about", "/pages/about.html"),
    ("contact", "/pages/contact.html"),
    ("cv", "/pages/cv.html"),
    ("blog", "/category/blog.html"),
)

# Sitemap Settings
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.6,
        "indexes": 0.6,
        "pages": 0.5,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    },
}

# Social widget
SOCIAL = (
    ("LinkedIn", "https://www.linkedin.com/in/erlene-rosowsky-91136431/"),
)

DEFAULT_PAGINATION = False

THEME = "themes/myidea"

# Generate typographic code
# requires packages: typogrify, typing-extensions
TYPOGRIFY = True
TYPOGRIFY_DASHES = "oldschool_inverted"

# SEO settings
SEO_REPORT = True  # generate report, excluded by .gitignore
SEO_ENHANCER = True  # These are the primary SEO features
SEO_ENHANCER_OPEN_GRAPH = False  # False is the default value for this feature
SEO_ENHANCER_TWITTER_CARDS = (
    False  # False is the default value for this feature
)

IMAGE_PROCESS = {
    "thumb": {
        "type": "image",
        "ops": [
            "crop 0 0 50% 50%",
            "scale_out 150 150 True",
            "crop 0 0 150 150",
        ],
    },
    "article-image": {
        "type": "image",
        "ops": ["scale_in 400 400 True"],
    },
    "crisp": {
        "type": "responsive-image",
        "srcset": [
            ("1x", ["scale_in 800 600 True"]),
            ("2x", ["scale_in 1600 1200 True"]),
            ("4x", ["scale_in 3200 2400 True"]),
        ],
        "default": "1x",
    },
    "large-photo": {
        "type": "responsive-image",
        "sizes": (
            "(min-width: 1200px) 800px, "
            "(min-width: 992px) 650px, "
            "(min-width: 768px) 718px, "
            "100vw"
        ),
        "srcset": [
            ("400w", ["scale_in 400 300 True"]),
            ("600w", ["scale_in 600 450 True"]),
            ("800w", ["scale_in 800 600 True"]),
            ("1600w", ["scale_in 1600 1200 True"]),
        ],
        "default": "800w",
    },
    "example-pict": {
        "type": "picture",
        "sources": [
            {
                "name": "scale",
                "media": "(min-width: 640px)",
                "srcset": [
                    ("640w", ["scale_in 640 480 True"]),
                    ("1024w", ["scale_in 1024 683 True"]),
                    ("1600w", ["scale_in 1600 1200 True"]),
                ],
                "sizes": "100vw",
            },
            {
                "name": "source-1",
                "srcset": [
                    ("1x", ["crop 100 100 200 200"]),
                    ("2x", ["crop 100 100 300 300"]),
                ],
            },
        ],
        "default": ("scale", "640w"),
    },
}
