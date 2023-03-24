# Effectiveness of Different Test Case Prioritization Methods Based on Coverage Criteria
In this project, we will compare the effectiveness of different kinds of test case prioritization methods in exposing faults via multiple coverage criteria. 

For each benchmark program, we will use test case prioritization methods to create test
suites according to the different coverage criteria.


For each created test suite, we will evaluate its fault-exposing potential by identifying the set of available faults that are exposed by the test suite.

## Generating test suites
To generate test suite, run

```shell
cd benchmarks
python3 coverage.py
```

## Evaluating fault-exposing potential
To evaluate fault-exposing potential, run

```
cd benchmarks
python3 test_coverage.py
```
## Test suites location
Each of the six test suites generated according to the six combinations are stored in their respective program folders.

For example, the location of the generated test suite for the "printtokens" program using total prioritization and branches coverage is:

```
class-project-noteamname/benchmarks/printtokens/total_coverage_branches.txt

```
