from seeds.seed_operators import seed as seed_operators


def run_seeds(*seed_names):
    seed_functions = {
        'operators': seed_operators,
    }

    for seed_name in seed_names:
        if seed_name in seed_functions:
            print(f'Seeding {seed_name}...')
            seed_functions[seed_name]()
        else:
            print(f'Seed {seed_name} not found.')
