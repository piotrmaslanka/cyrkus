# Cyrkus

Cyrkus is a very simple cluster health monitoring tool.

It consists of two parts: _redaction_ and _reporter_. Multiple _redaction_ instances
report the state to a single _redaction_.

_reporter_ is a part run on each system in the cluster. It connects to
_redaction_ and reports system health state to it. _redaction_ should run on
the computer that monitors the cluster health state. A _reporter_ should also
run on it - if you want it monitored that is.

Similarly to many of my concotions, it requires [Satella](https://github.com/piotrmaslanka/satella).
