# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from scipy.sparse import csr_matrix, lil_matrix
import torch


def random_sparse_binary_matrix(rows, cols, fill, min_entries_per_col) -> csr_matrix:
    retv = lil_matrix((rows, cols))

    if min_entries_per_col > 0:
        min_entries_per_col = min(rows, min_entries_per_col)
        rows_array = torch.arange(rows)
        rows_array_f = rows_array.to(dtype=torch.float)
        for c in range(cols):
            row_selection = rows_array[rows_array_f.multinomial(min_entries_per_col)]
            for r in row_selection:
                retv[r, c] = 1.0

    num_entries = int(fill * rows * cols)
    while retv.getnnz() < num_entries:
        col = int(torch.randint(cols, ()))
        row = int(torch.randint(rows, ()))
        retv[row, col] = 1.0

    return retv.tocsr()
