SUPPORT = 5
CONFIDENCE = 5

all: directories data 

rules:
	rm -f rule-output.txt
	./apriori/src/apriori -tr -s$(SUPPORT) -c$(CONFIDENCE) -R appearences.txt transactions.txt rule-output.txt

transactions:
	echo "Removing any old appearences and transaction files."
	rm -f appearences.txt
	rm -f transactions.txt
	python .py

directories: 
	mkdir -p reuters-dataset

data:
	wget -r --no-parent -A "*.sgm" http://web.cse.ohio-state.edu/~srini/674/public/reuters/ 
	find web.cse.ohio-state.edu/~srini/674/public/reuters/ -name '*.sgm' -exec mv {} reuters-dataset/ \;
	rm -rf web.cse.ohio-state.edu

clean-all:
	rm -rf reuters-dataset
	rm -f *.pyc
	rm -f appearences.txt
	rm -f transactions.txt

clean:
	rm -f rule-output.txt
	rm -rf *.pyc
