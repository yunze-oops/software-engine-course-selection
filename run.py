from system import CourseSelectionSystem 

def main():
    system = CourseSelectionSystem()

    while True:
        print("\n=== Course Selection System ===")
        print("1. Student Login")
        print("2. Create Student Account")
        print("3. Admin Login")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            student_id = input("Enter your student ID: ")
            password = input("Enter your password: ")

            if system.student_login(student_id, password):
                print("Student login successful!")

                while True:
                    print("\n=== Student Menu ===")
                    print("1. Select Course")
                    print("2. Delete Course")
                    print("3. Check Selected Courses")
                    print("4. Logout")

                    student_choice = input("Enter your choice (1-4): ")

                    if student_choice == "1":
                        system.student_select_course(student_id)
                    elif student_choice == "2":
                        system.student_delete_course(student_id)
                    elif student_choice == "3":
                        system.student_check_courses(student_id)
                    elif student_choice == "4":
                        break
                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Invalid student login.")

        elif choice == "2":
            student_id = input("Enter a new student ID: ")
            student_name = input("Enter the student name: ")
            password = input("Enter the password: ")

            system.create_student_account(student_id, student_name, password)
            print("Student account created successfully!")

        elif choice == "3":
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")

            if system.admin_login(admin_username, admin_password):
                print("Admin login successful!")

                while True:
                    print("\n=== Admin Menu ===")
                    print("1. Check All Students")
                    print("2. Check All Courses")
                    print("3. Add Course")
                    print("4. Delete Course")
                    print("5. Logout")

                    admin_choice = input("Enter your choice (1-5): ")

                    if admin_choice == "1":
                        system.admin_check_all_students()
                    elif admin_choice == "2":
                        system.admin_check_all_courses()
                    elif admin_choice == "3":
                        new_course_name = input("Enter the name of the new course: ")
                        system.admin_add_course(new_course_name)
                    elif admin_choice == "4":
                        system.admin_delete_course()
                    elif admin_choice == "5":
                        break
                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Invalid admin login.")

        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
    
    system.connection.close()


if __name__ == "__main__":
    main()

