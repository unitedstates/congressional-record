# Fixing run_tests.py

`run_tests.py` wasn't actually causing any tests to run. This change fixes that, but it is worth examining why it had stopped working.

## History of run_tests.py and Why It Broke

  Original working version (commits b7281c4 and 092458c):

```python
  import unittest
  from tests.test_parser import *

  if __name__ == '__main__':
      unittest.main()
```

  How it worked:
  - The from tests.test_parser import * line imported all test classes into the run_tests module's namespace
  - When unittest.main() ran, it discovered tests in the current module (run_tests.py)
  - Since the test classes were imported, they appeared to be defined in run_tests.py, so unittest.main() found and ran them

  Broken version (commit 9d2363b - Feb 2024 "add pre-commit hooks"):

```python
  import unittest

  if __name__ == "__main__":
      unittest.main()
```

  What changed:
  - The commit removed the from tests.test_parser import * line
  - This was likely done by an auto-formatter (black or similar) during the pre-commit hooks setup
  - Without the import, unittest.main() looks in the current module and finds nothing - hence 0 tests

  Why it was removed:
  - Using from X import * is considered bad practice (PEP 8 discourages it)
  - The linter/formatter likely flagged it as a code smell
  - The developer removed it to satisfy the linters but didn't realize it broke test discovery

 ## The Fix:

  The solution uses the proper unittest API for test discovery:
  ```python
  loader = unittest.TestLoader()
  suite = loader.discover('tests')
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
  ```

  This is the correct way to discover tests in a separate directory. It doesn't rely on namespace pollution from import *.

  So yes, unittest.main() worked in the past, but only because of the from tests.test_parser import * hack. When that was removed for 
  code quality reasons, the test runner broke.
