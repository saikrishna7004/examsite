from django_hosts import patterns, host

host_patterns = patterns('path.to',
    host(r'api', 'examproject.urls', name='api'),
    host(r'beta', 'examproject.urls', name='beta'),
)