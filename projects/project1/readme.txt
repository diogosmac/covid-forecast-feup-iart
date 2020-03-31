IART - TP01

Class:  3MIEIC01
Group:  Diogo Machado - up201706832
        Gonçalo Marantes - up201706917
        Leonardo Moura - up201706907

Google HashCode 2018 - Qualification Round
Self-Driving Rides

To run this project you need:
    - to have Python installed, with PIP;
    - to install the required dependencies of our project, using PIP:
        for that, you need only run
            pip install -r requirements.txt
        from the base directory of the project, on your terminal


After that, you can run either of the algorithms using:

    python main_hc.py <from_scratch> <input_file> - for the Hill Climbing algorithms
        - <from_scratch> can take two values: 0 or 1
            if it is 0, a greedy solution will be built first, and the algorithms will be ran from there
            if it is 1, the algorithms will be used from the starting point
        - <input_file> corresponds to the name of the dataset, with the following options:
            a_example
            b_should_be_easy
            c_no_hurry
            d_metropolis
            e_high_bonus

    python main_genetic.py <input_file> - for the Genetic Algorithm
        - <input_file> corresponds to the name of the dataset, with the following options:
            a_example
            b_should_be_easy
            c_no_hurry
            d_metropolis
            e_high_bonus
