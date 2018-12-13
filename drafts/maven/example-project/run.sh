jython -J-cp .:$(ls ./target/dependency/*.jar | xargs | sed 's/ /:/g') $@
