jython -J-cp .:$(ls ./target/dependency/*.jar | xargs | sed 's/ /:/g') jar_import_test.py
