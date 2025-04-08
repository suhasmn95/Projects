#include <iostream>
#include <string>
using namespace std;

class Person {
public:
    string name;
    Person* father;
    Person* mother;
    Person* child;
    Person* sibling;

    // Constructor
    Person(string name) {
        this->name = name;
        father = nullptr;
        mother = nullptr;
        child = nullptr;
        sibling = nullptr;
    }

    // Add a child to this person
    void addChild(Person* childPerson) {
        if (child == nullptr) {
            child = childPerson;
        } else {
            Person* current = child;
            while (current->sibling != nullptr) {
                current = current->sibling;
            }
            current->sibling = childPerson;
        }
    }

    // Recursive function to print the family tree
    void printTree(int level = 0) {
        for (int i = 0; i < level; i++) cout << "  ";
        cout << name << endl;

        if (child) child->printTree(level + 1);
        if (sibling) sibling->printTree(level);
    }
};

int main() {
    // Creating people
    Person* grandpa = new Person("Grandpa");
    Person* dad = new Person("Dad");
    Person* uncle = new Person("Uncle");
    Person* me = new Person("Me");
    Person* sister = new Person("Sister");

    // Building relationships
    grandpa->addChild(dad);
    grandpa->addChild(uncle);

    dad->addChild(me);
    dad->addChild(sister);

    // Display the family tree
    cout << "Family Tree:\n";
    grandpa->printTree();

    // Memory cleanup (not handled here)
    return 0;
}
