import java.util.Scanner;

public class age {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Ask for the user's age
        System.out.print("Please enter your age: ");
        int age = scanner.nextInt();

        // Determine the age category
        if (age >= 13 && age <= 19) {
            System.out.println("You are a teenager.");
        } else if (age >= 20 && age <= 29) {
            System.out.println("You are a young adult.");
        } else if (age >= 30 && age <= 64) {
            System.out.println("You are an adult.");
        } else if (age >= 65 && age <= 80) {
            System.out.println("You are a senior.");
        } else if (age > 80) {
            System.out.println("You are very old.");
        } else {
            System.out.println("You are a child.");
        }

        scanner.close();
    }
}
