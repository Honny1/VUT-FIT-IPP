from interpretr_libs.expections import StatsMissingFile


class Stats:
    def __init__(self, file, stats_ordered):
        self.file = file
        self.stats_ordred = stats_ordered
        if self.file is None and self.stats_ordred:
            raise StatsMissingFile("Missing parametr stats")

        self.insts_num = 0
        self.hot_nums = {}
        self.var_max = 0

    def _get_vars_sum(self, engine):
        sum_vars = len(engine.GF.keys())
        if engine.TF is not None:
            sum_vars += len(engine.TF.keys())
        for frame in engine.stack_LF:
            sum_vars += len(frame.keys())
        return sum_vars

    def _get_hottest_instruction(self):
        self.hot_nums = dict(sorted(self.hot_nums.items()))
        return max(self.hot_nums, key=self.hot_nums.get)

    def save_stats(self):
        for stat in self.stats_ordred:
            if stat == "--insts":
                self.file.writelines(f"{self.insts_num}\n")
            if stat == "--hot":
                self.file.writelines(f"{self._get_hottest_instruction()}\n")
            if stat == "--vars":
                self.file.writelines(f"{self.var_max}\n")

    def update_stats(self, engine, instruction):
        if instruction.opcode not in ("LABEL", "BREAK", "DPRINT"):
            self.insts_num += 1
        if instruction.order in self.hot_nums:
            self.hot_nums[instruction.order] += 1
        else:
            self.hot_nums[instruction.order] = 1
        new_var_sum = self._get_vars_sum(engine)
        if new_var_sum > self.var_max:
            self.var_max = new_var_sum
