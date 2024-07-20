[app]
# (string) Title of your application
title = Anti-Phishing App for Tokyo 2025

# (string) Package name
package.name = anti_phishing_app

# (string) Package domain (e.g., org.myapp)
package.domain = org.example

# (string) The name of your application
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*, model/*, *.csv

# (list) List of application requirements
requirements = python3,kivy,plyer,scikit-learn,joblib

# (list) List of permissions
android.permissions = RECEIVE_SMS, READ_SMS, READ_PHONE_STATE

# (list) List of build dependencies
android.libraries = plyer

# (string) Path to the build directory
build.dir = build

# (bool) Whether to keep the build directory for debugging
clean_build = 1

# (string) The version of your application
version = 1.0.0
