import numpy as np


def simplex_method(z, constraints, rhs):
    try:
        # Inisialisasi tabel Simpleks
        num_vars = len(z)
        num_constraints = len(constraints)

        table = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
        table[:-1, :num_vars] = constraints
        table[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
        table[:-1, -1] = rhs
        table[-1, :num_vars] = -np.array(z)

        # Iterasi Simpleks
        while True:
            # Cek optimalitas
            if all(val >= 0 for val in table[-1, :-1]):
                break

            # Temukan pivot kolom
            pivot_col = np.argmin(table[-1, :-1])
            if all(row[pivot_col] <= 0 for row in table[:-1]):
                raise ValueError("Masalah tidak memiliki solusi terbatas.")

            # Temukan pivot baris
            ratios = []
            for i in range(num_constraints):
                if table[i, pivot_col] > 0:
                    ratios.append(table[i, -1] / table[i, pivot_col])
                else:
                    ratios.append(float('inf'))
            pivot_row = np.argmin(ratios)

            # Pivoting
            pivot_element = table[pivot_row, pivot_col]
            table[pivot_row, :] /= pivot_element
            for i in range(len(table)):
                if i != pivot_row:
                    table[i, :] -= table[i, pivot_col] * table[pivot_row, :]

        # Ekstrak solusi
        solutions = np.zeros(num_vars)
        for i in range(num_vars):
            col = table[:-1, i]
            if np.count_nonzero(col == 1) == 1 and np.count_nonzero(col) == 1:
                row = np.where(col == 1)[0][0]
                solutions[i] = table[row, -1]

        z_value = table[-1, -1]
        return solutions, z_value
    except Exception as e:
        print(f"Error: {e}")
        return None, None
