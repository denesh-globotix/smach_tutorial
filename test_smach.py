#!/usr/bin/env python3
import rospy
import smach
from smach import State

# define state Foo
class Code(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['time_to_sleep','done'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        if self.counter < 3:
            self.counter += 1
            rospy.loginfo("Time to sleep")
            return 'time_to_sleep'
        else:
            return 'done'


# define state Bar
class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['continue_coding'])

    def execute(self, userdata):
        rospy.loginfo('Done sleeping get back to coding')
        return 'continue_coding'
        



def initialiseStateMachine():
    # Initialise the ros node
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine with 2 outcomes?
    sm = smach.StateMachine(outcomes=['project_delivered', 'burned_out'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('CODE', Code(), 
                               transitions={'time_to_sleep':'SLEEP', 
                                            'done':'project_delivered'})
        smach.StateMachine.add('SLEEP', Sleep(), 
                               transitions={'continue_coding':'CODE'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    initialiseStateMachine()
