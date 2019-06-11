from collections import deque
from defaults import Ancestors


class Family:

    @staticmethod
    def breedable(m1,m2):
        return not Family.are_family(m1, m2)

    @staticmethod
    def are_family(member_1, member_2):
        # print(f"===START:: Checking breedability between {member_1} and {member_2}")

        (m1_father, m1_mother) = member_1.parents if member_1.parents else ('', '')
        (m2_father, m2_mother) = member_2.parents if member_2.parents else ('', '')

        is_family = False
        # checks for siblings/half siblings directly
        if m1_father and m1_mother and m2_father and m2_mother and (m1_father == m2_father or m1_mother == m2_mother):
            is_family = True
        elif Family.trace_common_family(member_1, member_2, 1):
            is_family = True

        else:
            is_family = False

        # print(f"===END:: {member_1} and {member_2} are{' not' if not is_family else ''} a family")

        return is_family

    @staticmethod
    def trace_common_family(members_to_check_against, member, depth, back_ref=deque(maxlen=3)):
        """Checks if member is a close family member based on Ancestors.DESCENDANCY_DEPTH"""

        # print(f"Checking {member} at depth level:{str(depth)} against {Nature.print_individual(members_to_check_against)}")
        if abs(depth) > Ancestors.DESCENDANCY_DEPTH:
            # print("Max depth reached")
            return False
        elif not members_to_check_against:
            # print("No further members to check")
            return False
        elif type(members_to_check_against) == tuple or\
                type(members_to_check_against) == list or\
                type(members_to_check_against) == set:

            if member in members_to_check_against:
                # print("Family member found")
                return True
            else:
                family_found = False

                for member_to_check in members_to_check_against:
                    qpop = back_ref.popleft() if len(back_ref) > 0 else ''
                    if qpop:
                        back_ref.appendleft(qpop)

                    if qpop != member_to_check:
                        back_ref.append(member_to_check)
                        family_found = Family.trace_common_family(member_to_check,
                                                                  member, abs(depth) + 1, back_ref)
                    # else:
                        # print(f"{member_to_check} skipped due to back reference {str(back_ref)}")

                    if family_found:
                        return True

                return family_found

        else:
            q1 = back_ref.copy()
            q2 = back_ref.copy()
            if len(back_ref) == 0:
                q1.append(members_to_check_against)
                q2.append(members_to_check_against)

            return Family.trace_common_family(members_to_check_against.parents,
                                              member, abs(depth),  q1) or \
                   Family.trace_common_family(members_to_check_against.children,
                                              member, abs(depth),  q2)


    @staticmethod
    def chose_female_no_inbreed(male, female_population):
        for female in female_population:
            if not female.is_pregnent and not female.strength < 0:
                # check inbreeding
                if Family.breedable(male, female):
                    return female
