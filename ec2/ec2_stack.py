from aws_cdk import core, aws_ec2 as ec2, aws_efs as efs

class Ec2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "MyVpc",
            cidr="10.0.0.0/16",
            max_azs=2
        )

        # Create EFS file system
        efs_sg = ec2.SecurityGroup(self, "EfsSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True  
        )

        efs_fs = efs.FileSystem(self, "MyEFS",
            vpc=vpc,
            encrypted=True,
            security_group=efs_sg 
        )

        # Create EC2 instance
        instance_sg = ec2.SecurityGroup(self, "InstanceSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True  
        )

        instance = ec2.Instance(self, "MyInstance",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            security_group=instance_sg  
        )

       
        efs_sg.add_ingress_rule(
            peer=instance_sg,
            connection=ec2.Port.tcp(2049),
            description="Allow NFS traffic from EC2 instance"
        )

        # Mount EFS to EC2 instance
        instance.user_data.add_commands(
            "yum install -y amazon-efs-utils",
            f"mkdir -p /mnt/efs",
            f"mount -t efs {efs_fs.file_system_id}:/ /mnt/efs"
        )
