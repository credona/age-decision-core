<h1>Security Policy</h1>

This document covers repository-specific security constraints for Age Decision Core.

For ecosystem-wide policy and coordinated disclosure guidance, see:
https://github.com/credona/age-decision/blob/main/SECURITY.md

<hr>

<h2>Local security scope</h2>

Security reports in this repository may concern:

- Core request handling and validation
- `/estimate` contract leakage risks
- unsafe logging of image payloads
- metadata or trace identifier leakage
- model file path and mount misconfiguration

<hr>

<h2>Local privacy constraints</h2>

Core should not:

- persist uploaded images by default
- expose estimated age in public responses
- expose raw model confidence in public responses
- log raw image bytes or base64 payloads
- commit model binaries or secrets to Git
