default:
  just --list

run:
  flask --app bitlypy --debug run

test:
  python -m pytest tests/
