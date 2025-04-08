#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the structure for a person
typedef struct Person {
    char name[50];
    struct Person* father;
    struct Person* mother;
    struct Person* child;
    struct Person* sibling;
} Person;

// Function to create a new person
Person* createPerson(const char* name) {
    Person* newPerson = (Person*)malloc(sizeof(Person));
    strcpy(newPerson->name, name);
    newPerson->father = NULL;
    newPerson->mother = NULL;
    newPerson->child = NULL;
    newPerson->sibling = NULL;
    return newPerson;
}

// Add a child to a parent (for simplicity, this assumes one parent)
void addChild(Person* parent, Person* child) {
    if (parent->child == NULL) {
        parent->child = child;
    } else {
        Person* sibling = parent->child;
        while (sibling->sibling != NULL) {
            sibling = sibling->sibling;
        }
        sibling->sibling = child;
    }
}

// Print the family tree (recursive)
void printFamilyTree(Person* person, int level) {
    if (person == NULL) return;
    
    for (int i = 0; i < level; i++) printf("  ");
    printf("%s\n", person->name);

    printFamilyTree(person->child, level + 1);
    printFamilyTree(person->sibling, level);
}

int main() {
    // Create family members
    Person* grandFather = createPerson("Grandfather");
    Person* father = createPerson("Father");
    Person* uncle = createPerson("Uncle");
    Person* child1 = createPerson("Child1");
    Person* child2 = createPerson("Child2");

    // Set relationships
    addChild(grandFather, father);
    addChild(grandFather, uncle);

    addChild(father, child1);
    addChild(father, child2);

    // Print the family tree starting from the grandfather
    printf("Family Tree:\n");
    printFamilyTree(grandFather, 0);

    // Free memory (not shown here for brevity)
    return 0;
}
