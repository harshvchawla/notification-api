"""empty message

Revision ID: 0033_correct_permission_enums
Revises: 0032_update_permission_to_enum
Create Date: 2016-03-02 15:00:25.358153

"""

# revision identifiers, used by Alembic.
revision = '0033_correct_permission_enums'
down_revision = '0032_update_permission_to_enum'

import uuid
from datetime import datetime
from alembic import op
import sqlalchemy as sa


def add_default_permissions(conn, permissions):
    user_services = conn.execute("SELECT * FROM user_to_service").fetchall()
    for entry in user_services:
        for p in permissions:
            id_ = uuid.uuid4()
            created_at = datetime.now().isoformat().replace('T', ' ')
            conn.execute((
                "INSERT INTO permissions (id, user_id, service_id, permission, created_at)"
                " VALUES ('{}', '{}', '{}', '{}', '{}')").format(id_, entry[0], entry[1], p, created_at))


def upgrade():
    # Since there are no specific permissions set for services yet
    # we can just remove all and re-add all.
    ### commands auto generated by Nick - please adjust! ###
    new_permissions = ['manage_users',
                       'manage_templates',
                       'manage_settings',
                       'send_texts',
                       'send_emails',
                       'send_letters',
                       'manage_api_keys',
                       'access_developer_docs']
    conn = op.get_bind()
    conn.execute("DELETE FROM permissions")
    op.drop_constraint('uix_service_user_permission', 'permissions', type_='unique')
    op.drop_column('permissions', 'permission')
    try:
        sa.Enum(name='permission_types').drop(conn, checkfirst=False)
    except:
        pass
    permission_types = sa.Enum(*new_permissions, name='permission_types')
    permission_types.create(op.get_bind())
    op.add_column('permissions', sa.Column('permission', permission_types, nullable=False))
    add_default_permissions(conn, new_permissions)
    op.alter_column('permissions', 'permission', nullable=False)
    op.create_unique_constraint('uix_service_user_permission', 'permissions', ['service_id', 'user_id', 'permission'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Nick - please adjust! ###
    old_permissions = ['manage_service',
                        'send_messages',
                        'manage_api_keys',
                        'manage_templates',
                        'manage_team',
                        'view_activity']
    conn = op.get_bind()
    conn.execute("DELETE FROM permissions")
    op.drop_constraint('uix_service_user_permission', 'permissions', type_='unique')
    op.drop_column('permissions', 'permission')
    try:
        sa.Enum(name='permission_types').drop(conn, checkfirst=False)
    except:
        pass
    permission_types = sa.Enum(*old_permissions, name='permission_types')
    permission_types.create(op.get_bind())
    op.add_column('permissions', sa.Column('permission', permission_types, nullable=False))
    add_default_permissions(conn, old_permissions)
    op.alter_column('permissions', 'permission', nullable=False)
    op.create_unique_constraint('uix_service_user_permission', 'permissions', ['service_id', 'user_id', 'permission'])
    ### end Alembic commands ###